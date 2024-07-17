#!/usr/bin/env -S python3 -O
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


import asyncio
from binascii import a2b_base64
from enum import Enum
import inspect
import logging
from queue import Empty, Full, Queue
import time
from typing import NamedTuple

import slapdsock.message
from slapdsock.service import SlapdSockServer
from ldap0.typehints import EntryMixed
from slapdsock.handler import InternalErrorResponse, SlapdSockHandler, SlapdSockHandlerError
from slapdsock.message import CONTINUE_RESPONSE, RESULTRequest
from ldap0.res import decode_response_ctrls
from ldap0.controls.readentry import PostReadControl, PreReadControl
from slapdsock.service import threading


TIMEOUT_RESPONSE = (
    "RESULT\ncode: 51\nmatched: <DN>\ninfo: slapdsocklistener busy sending messages to the message queue\n"
)


logger = logging.getLogger(__name__)


class RequestType(str, Enum):
    add = "ADD"
    modify = "MODIFY"
    modrdn = "MODRDN"
    delete = "DELETE"


class LDAPMessage(NamedTuple):
    request_type: RequestType
    binddn: str
    old: EntryMixed | None
    new: EntryMixed | None
    message_id: int = 0
    request_id: str = ""


def is_refint_request(request_lines: list[bytes]) -> bool:
    """
    matches the default refint modifiersName
    in theory this could be changed / broken by a custom name configuration in the slapd.conf
    """
    modifiers_name = [r for r in request_lines if r.startswith(b"modifiersName: ")]
    if not modifiers_name:
        return False
    return modifiers_name[0].endswith(b"cn=Referential Integrity Overlay")


class ReasonableSlapdSockHandler(SlapdSockHandler):
    unittest = False

    def __call__(self, *args, **kwargs):
        """
        Handle a request.

        See https://stackoverflow.com/questions/21631799/how-can-i-pass-parameters-to-a-requesthandler
        """
        super().__init__(*args, **kwargs)

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handle the incoming request
        """
        self.request_timestamp = time.time()
        self.server._req_count += 1
        msgid = None
        # Generate basic log prefix here
        self.log_prefix = str(id(self))
        reqtype = "-/-"

        try:  # -> Exception
            self._log(logging.DEBUG, "----- incoming request -----")
            request_data = b""
            try:
                while True:
                    data = await reader.read(1024)
                    request_data += data
                    if not data or data[-2:] == b"\n\n":
                        break
            except OSError as exc:
                self._log(logging.ERROR, "Error reading request data: %s", exc)
                self._log(logging.ERROR, "Request data so far: %r", request_data)
                return

            if __debug__:
                # Security advice:
                # Request data can contain clear-text passwords!
                self._log(logging.DEBUG, ", raw_socket_request (length: %d) = %r", len(request_data), request_data)
            self.server._bytes_received += len(request_data)
            req_lines = request_data.split(b"\n")
            # Extract request type
            reqtype = req_lines[0].decode("ascii")
            self._log(logging.DEBUG, "reqtype = %r", reqtype)
            # Get the request message class
            if not reqtype:
                self._log(logging.DEBUG, "ignoring empty socket request: %s", req_lines)
                return
            request_class = getattr(slapdsock.message, "%sRequest" % reqtype)
            self._log(logging.DEBUG, ", request.class=%r", request_class)
            # Extract the request message
            sock_req = request_class(req_lines)
            # Update request counter for request type
            self.server._req_counters[reqtype.lower()] += 1
            if __debug__:
                # Security advice:
                # Request data can contain sensitive data
                # (e.g. BIND with password) => never run in debug mode!
                self._log(logging.DEBUG, "sock_req = %r // %r", sock_req, sock_req.__dict__)
            # Generate the request specific log prefix here
            self.log_prefix = sock_req.log_prefix(self.log_prefix)
            msgid = sock_req.msgid

            try:  # -> SlapdSockHandlerError
                # Get the handler method in own class
                handle_method = getattr(self, "do_%s" % reqtype.lower())
                # Let the handler method generate a response message
                if inspect.iscoroutinefunction(handle_method):
                    response = await handle_method(sock_req)
                else:
                    response = handle_method(sock_req)
            except SlapdSockHandlerError as handler_exc:
                if self.unittest:
                    raise
                handler_exc.log(self.server.logger)
                response = handler_exc.response or InternalErrorResponse(msgid)

        except Exception as error:
            if self.unittest:
                raise
            self._log(
                logging.ERROR,
                "Unhandled exception during processing request: %s",
                msgid,
                exc_info=error,
                stack_info=True,
            )
            response = InternalErrorResponse(msgid)
        try:
            # Serialize the response instance
            if isinstance(response, str):
                response_str = response.encode("utf-8")
            else:
                response_str = bytes(response)
            self._log(logging.DEBUG, "response_str = %r", response_str)
            if not response_str and reqtype not in {"ENTRY", "RESULT", "UNBIND"}:
                self._log(logging.ERROR, "empty response string for request: %s", request_data)
            if response_str:
                # TODO: don't send response that triggers tracebacks.
                try:
                    self.request.sendall(response_str)
                except (BrokenPipeError, OSError) as error:
                    self._log(
                        logging.ERROR,
                        "socket response error for request: %s, response: %s",
                        request_data,
                        response_str,
                        exc_info=error,
                    )
        except Exception:
            if self.unittest:
                raise
            self._log(logging.ERROR, "Unhandled exception while sending response:", exc_info=True)
        else:
            response_delay = time.time() - self.request_timestamp
            self.server.update_monitor_data(len(response_str), response_delay)
            self._log(logging.DEBUG, "response_delay = %0.3f ms", response_delay * 1000)
        # end of handle()


class LDAPHandler(ReasonableSlapdSockHandler):
    """
    This handler simply returns CONTINUE+LF for every sockops request
    and empty string for sockresps and unbind requests.

    This is handy to be used as safe base class for own custom handler
    to make sure each back-sock request is always answered in
    case of misconfigured "overlay sock" section.
    """

    def __init__(
        self,
        ldap_base: str,
        ldap_threads: int,
        ignore_temporary: bool,
        outgoing_queue: asyncio.Queue,
        backpressure_wait_timeout: int,
    ):
        # workaround for not using the 'socketserver' API anymore
        self.server = SlapdSockServer(
            "/tmp/___sock",
            self.__class__,
            logger,
            average_count=10,
            socket_timeout=1,
            socket_permissions="600",
            allowed_uids=(0,),
            allowed_gids=(0,),
            thread_pool_size=1,
        )

        self.backpressure_wait_timeout = backpressure_wait_timeout

        self.journal_key = 0
        self.journal_key_mutex = threading.Lock()
        self.outgoing_queue = outgoing_queue
        self.request_throttling_mutex = threading.Lock()

        self.ignore_temporary = ignore_temporary

        self.temporary_dn_identifier = f",cn=temporary,cn=univention,{ldap_base}"

        # NOTE: Be careful when extending the Queue maxsize!
        # It's not clear that RESULT responses come in the same order as the
        # requests, so in do_result the timestamps need to be matched with (msgid, connid).
        # Also, then several parallel threads may run do_result, so that may need
        # to be somehow serialized to maintain order of ops towards NATS.
        # NOTE: (msgid, connid) are recycled after slapd restart (connid seems
        # to start at 1000 again).
        self.legacy_backpressure_queue = Queue(maxsize=1)

    def filter_temporary_dn(self, request):
        return request.dn.endswith(self.temporary_dn_identifier)

    def request_throttling(self, request) -> bool:
        self.legacy_add_backpressure(request)
        if not self.outgoing_queue.full():
            return True

        if not self.request_throttling_mutex.acquire(timeout=self.backpressure_wait_timeout):
            self._log(logging.INFO, "Timed out waiting for the outgoing queue. message id: %s", request.msgid)
            return False
        try:
            max_loops = int(2 / 0.1)
            for _ in range(max_loops):
                if not self.outgoing_queue.full():
                    return True
                time.sleep(0.1)
            error_time = time.perf_counter()
            self._log(
                logging.ERROR,
                "LDAP write operation was aborted because the backpressure did not decrease within the timeout"
                "message id: %s, time: %s",
                request.msgid,
                error_time,
            )
            # "do_add = %s failed because no LDAPHandler seat was available within the timeout"
            return False
        finally:
            self.request_throttling_mutex.release()

    def legacy_add_backpressure(self, request) -> bool:
        if not __debug__:
            return True
        if self.ignore_temporary and self.filter_temporary_dn(request):
            return True
        if is_refint_request(request._req_lines):
            self._log(logging.DEBUG, "ignoring referential integrity modify request: %s", request.msgid)
            return True
        try:
            self.legacy_backpressure_queue.put_nowait((request.connid, request.msgid, time.perf_counter()))
        except Full:
            try:
                orphan = self.legacy_backpressure_queue.get_nowait()
            except Empty:
                self._log(logging.ERROR, "congestion has cleared up in the mean-time")

                return True

            error_time = time.perf_counter()
            self._log(
                logging.ERROR,
                "backpressure_queue full, "
                "this suggests a failure in synchronizing the previous pre- and post- hook "
                "current message id: %s, time: %s orphaned backpressure_queue item: %r",
                request.msgid,
                error_time,
                orphan,
            )
            return True
        self._log(
            logging.DEBUG,
            "added new element to backpressure_queue. new size: %s",
            self.legacy_backpressure_queue.qsize(),
        )
        return True

    def legacy_release_backpressure(self, msgid: int) -> None:
        if not __debug__:
            return
        response_time = time.perf_counter()
        try:
            (_, _, request_time) = self.legacy_backpressure_queue.get_nowait()  # signal one seat is free
        except Empty:
            self._log(
                logging.ERROR,
                "no in flight request found in backpressure_queue "
                "this suggests a failure in synchronizing the pre- and post- hook for the current message "
                "current message id: %s, time: %s",
                msgid,
                response_time,
            )
            return
        self._log(logging.INFO, "processing time  = %s", round(response_time - request_time, 6))

    def do_add(self, request):
        """
        ADD
        """
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE

        self._log(logging.DEBUG, "do_add = %s", request.msgid)
        return CONTINUE_RESPONSE

    def do_bind(self, request):
        """
        BIND
        """
        self._log(logging.DEBUG, "do_bind = %s", request.msgid)
        return CONTINUE_RESPONSE

    def do_compare(self, request):
        """
        COMPARE
        """
        _ = (self, request)  # pylint dummy
        return CONTINUE_RESPONSE

    def do_delete(self, request):
        """
        DELETE
        """
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE

        self._log(logging.DEBUG, "do_delete = %s", request.msgid)
        return CONTINUE_RESPONSE

    def do_modify(self, request):
        """
        MODIFY
        """
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE

        self._log(logging.DEBUG, "do_modify = %s", request.msgid)
        return CONTINUE_RESPONSE

    def do_modrdn(self, request):
        """
        MODRDN
        """
        self._log(logging.DEBUG, "do_modrdn = %s", request.msgid)
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE

        self._log(logging.DEBUG, "do_modrdn = %s", request.msgid)
        return CONTINUE_RESPONSE

    def do_search(self, request):
        """
        SEARCH
        """
        _ = (self, request)  # pylint dummy
        return CONTINUE_RESPONSE

    def do_unbind(self, request):
        """
        UNBIND
        """
        _ = (self, request)  # pylint dummy
        return ""

    async def do_result(self, request: RESULTRequest):
        # Ignore results from read requests
        _ = (self, request)  # pylint dummy
        if getattr(request, "dn", None) is None:
            # A search result or anything where RESULTRequest._parse_ldif didn't find anything.
            return ""

        if is_refint_request(request._req_lines):
            self._log(logging.DEBUG, "ignoring memberOf do_result request")
            return ""

        # ignore temporary dn modify results (if configured)
        self._log(logging.DEBUG, "do_result = %s", request.msgid)
        if self.ignore_temporary and self.filter_temporary_dn(request):
            self._log(logging.INFO, "ignoring dn = %s", request.dn)
            return ""

        # Parse result request type
        self._log(logging.INFO, "dn = %s", request.dn)
        if request.parsed_ldif:
            self._log(logging.DEBUG, "parsed_ldif = %s", request.parsed_ldif)
            if isinstance(request.parsed_ldif, list):
                reqtype = RequestType.modify
            elif b"newrdn" in request.parsed_ldif:
                reqtype = RequestType.modrdn
            else:
                reqtype = RequestType.add
        elif request.parsed_ldif is None:
            reqtype = RequestType.delete
        else:
            self._log(
                logging.INFO,
                "could not parse the request type = %s" % (request.parsed_ldif),
            )
            raise ValueError()
        self._log(logging.DEBUG, "reqtype = %s", reqtype)
        self._log(logging.DEBUG, "parsed_ldif = %s", request.parsed_ldif)

        if request.code == 0:
            # get the old and new objects from the ldap controls
            self._log(logging.INFO, "binddn = %s", request.binddn)
            self._log(logging.DEBUG, "ctrls = %s", request.ctrls)
            ctrls = [
                (control_type, criticality, a2b_base64(control_value))
                for (control_type, criticality, control_value) in request.ctrls
            ]
            ctrls = decode_response_ctrls(ctrls)

            new = None
            old = None
            for ctrl in ctrls:
                if isinstance(ctrl, PostReadControl):
                    new = ctrl.res.entry_as
                    self._log(logging.INFO, "PostRead entry_as = %s", ctrl.res.entry_as)
                elif isinstance(ctrl, PreReadControl):
                    old = ctrl.res.entry_as
                    self._log(logging.INFO, "PreRead entry_as = %s", ctrl.res.entry_as)
            if not old and not new:
                self._log(
                    logging.WARNING,
                    "Missing old or new object in socket request, add the necessary ldap controls to all clients.",
                )

            self._log(
                logging.INFO,
                "Call NATS for %s operation on dn = %s" % (reqtype, request.dn),
            )
            ldap_message = LDAPMessage(reqtype, request.binddn, old, new, request.msgid, "TODO")

            # Write LDAP transaction to journal
            self._log(logging.DEBUG, "Write %s request on dn = %s to internal journal" % (reqtype, request.dn))
            with self.journal_key_mutex:
                # TODO: Write the `ldap_message` into the sqlite journal!
                # sqlite.put(key=self.journal_key, value=ldap_message)
                self.journal_key += 1

            timeout = time.time() + 5
            while time.time() < timeout:
                try:
                    self.outgoing_queue.put_nowait(ldap_message)
                    break
                except asyncio.QueueFull:
                    await asyncio.sleep(0.05)
            else:
                self._log(logging.ERROR, "timeout putting message into outgoing_queue")
                raise Empty

        else:
            self._log(logging.INFO, "ignoring op with RESULT code = %s", request.code)

        self.legacy_release_backpressure(request.msgid)

        return ""

    def do_entry(self, request):
        """
        ENTRY
        """
        _ = (self, request)  # pylint dummy
        self._log(logging.DEBUG, "do_entry = %s", request)
        return ""

    def do_extended(self, request):
        """
        EXTERNAL
        """
        _ = (self, request)  # pylint dummy
        return CONTINUE_RESPONSE

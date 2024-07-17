# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import threading
import time
from binascii import a2b_base64
from queue import Empty, Full, Queue

from ldap0.controls.readentry import PostReadControl, PreReadControl
from ldap0.res import decode_response_ctrls

from slapdsock.handler import SlapdSockHandler
from slapdsock.log import request_id
from slapdsock.message import (
    CONTINUE_RESPONSE,
    ADDRequest,
    DELETERequest,
    MODIFYRequest,
    MODRDNRequest,
    RESULTRequest,
    SockResponse,
)

from .models import LDAPMessage, RequestType

TIMEOUT_RESPONSE = (
    "RESULT\ncode: 51\nmatched: <DN>\ninfo: slapdsocklistener busy sending messages to the message queue\n"
)

logger = logging.getLogger(__name__)


class LDAPHandler(SlapdSockHandler):
    def __init__(
        self,
        ldap_base: str,
        ignore_temporary: bool,
        outgoing_queue: asyncio.Queue,
        backpressure_wait_timeout: int,
    ):
        super().__init__()
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

    @staticmethod
    def is_refint_request(request_lines: list[bytes]) -> bool:
        """
        matches the default refint modifiersName
        in theory this could be changed / broken by a custom name configuration in the slapd.conf
        """
        for line in request_lines:
            if line.startswith(b"modifiersName: ") and line.endswith(b"cn=Referential Integrity Overlay"):
                return True
        return False

    def filter_temporary_dn(self, request):
        return request.dn.endswith(self.temporary_dn_identifier)

    def request_throttling(self, request) -> bool:
        self.legacy_add_backpressure(request)
        if not self.outgoing_queue.full():
            return True

        if not self.request_throttling_mutex.acquire(timeout=self.backpressure_wait_timeout):
            logger.info("Timed out waiting for the outgoing queue. message id: %s", request.msgid)
            return False
        try:
            max_loops = int(2 / 0.1)
            for _ in range(max_loops):
                if not self.outgoing_queue.full():
                    return True
                time.sleep(0.1)
            error_time = time.perf_counter()
            logger.error(
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
        if self.is_refint_request(request._req_lines) and request.msgid == 0:
            logger.debug("Ignoring referential integrity modify request.")
            return True
        try:
            self.legacy_backpressure_queue.put_nowait((request.connid, request.msgid, time.perf_counter()))
        except Full:
            try:
                orphan = self.legacy_backpressure_queue.get_nowait()
            except Empty:
                logger.error("Congestion has cleared up in the mean-time.")

                return True

            error_time = time.perf_counter()
            logger.error(
                "Backpressure_queue full. This suggests a failure in synchronizing the previous pre- and "
                "post-hook. Current message id: %r, time: %s orphaned backpressure_queue item: %r",
                request.msgid,
                error_time,
                orphan,
            )
            return True
        logger.debug(
            "Added new element to backpressure_queue. New size: %r",
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
            logger.error(
                "no in flight request found in backpressure_queue "
                "this suggests a failure in synchronizing the pre- and post- hook for the current message "
                "current message id: %s, time: %s",
                msgid,
                response_time,
            )
            return
        logger.debug("Request-Response duration: %.2f ms", (response_time - request_time) * 1000)

    async def do_add(self, request: ADDRequest) -> bytes | str | SockResponse:
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_delete(self, request: DELETERequest) -> bytes | str | SockResponse:
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_modify(self, request: MODIFYRequest) -> bytes | str | SockResponse:
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_modrdn(self, request: MODRDNRequest) -> bytes | str | SockResponse:
        if not self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_result(self, request: RESULTRequest) -> bytes | str | SockResponse:
        # Ignore results from read requests
        if getattr(request, "dn", None) is None:
            # A search result or anything where RESULTRequest._parse_ldif didn't find anything.
            return ""

        if self.is_refint_request(request._req_lines) and request.msgid == 0:
            logger.debug("Ignoring referential integrity modify result.")
            return ""

        # ignore temporary dn modify results (if configured)
        if self.ignore_temporary and self.filter_temporary_dn(request):
            logger.debug("Ignoring temporary object %r.", request.dn)
            return ""

        # Parse result request type
        if request.parsed_ldif:
            if isinstance(request.parsed_ldif, list):
                reqtype = RequestType.modify
            elif b"newrdn" in request.parsed_ldif:
                reqtype = RequestType.modrdn
            else:
                reqtype = RequestType.add
        elif request.parsed_ldif is None:
            reqtype = RequestType.delete
        else:
            logger.error("Could not parse the request type: %r", request.parsed_ldif)
            raise ValueError()
        logger.debug("reqtype: %r | parsed_ldif: %r", reqtype, request.parsed_ldif)

        if request.code == 0:
            # get the old and new objects from the ldap controls
            logger.debug("binddn: %r | ctrls: %r", request.binddn, request.ctrls)
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
                    logger.debug("PostRead entry_as = %s", ctrl.res.entry_as)
                elif isinstance(ctrl, PreReadControl):
                    old = ctrl.res.entry_as
                    logger.debug("PreRead entry_as = %s", ctrl.res.entry_as)
            if not old and not new:
                logger.warning(
                    "Missing old or new object in socket request, add the necessary ldap controls to all clients."
                )
            if reqtype == RequestType.modify and not old:
                logger.warning("Missing 'old' in MODIFY operation on %r.", request.dn)

            ldap_message = LDAPMessage(reqtype, request.binddn, old, new, request.msgid, request_id.get())

            # Write LDAP transaction to journal
            logger.debug("Writing %r request on DN %r to internal journal.", reqtype, request.dn)
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
                logger.error("Timeout putting message into outgoing_queue.")
                raise Empty

        else:
            logger.warning(
                "Ignoring RESULT response with code %r. msgid: %r info: %r",
                request.code,
                request.msgid,
                request.info if hasattr(request, "info") else "n/a",
            )
            logger.debug(f"{request.__dict__=}")

        self.legacy_release_backpressure(request.msgid)

        return ""

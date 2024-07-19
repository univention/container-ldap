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


class LDAPReciever(SlapdSockHandler):
    def __init__(
        self,
        ldap_base: str,
        ignore_temporary: bool,
        outgoing_queue: asyncio.Queue,
        backpressure_wait_timeout: float,
    ):
        super().__init__()
        self.backpressure_wait_timeout = backpressure_wait_timeout
        self.journal_key = 0
        self.journal_key_mutex = threading.Lock()
        self.outgoing_queue = outgoing_queue
        self.request_throttling_mutex = asyncio.Lock()
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

    async def request_throttling(self, request) -> bool:
        self.legacy_add_backpressure(request)
        if not self.outgoing_queue.full():
            return True

        try:
            logger.info(
                "The outgoing queue is full. Waiting for a maximum of %s seconds. message id: %s",
                self.backpressure_wait_timeout,
                request.msgid,
            )
            await asyncio.wait_for(self.request_throttling_mutex.acquire(), self.backpressure_wait_timeout * 0.8)
        except asyncio.TimeoutError:
            logger.info("Timed out waiting for the outgoing queue. message id: %s", request.msgid)
            return False

        try:
            max_loops = max(int(self.backpressure_wait_timeout * 0.2 / 0.1), 1)
            for _ in range(max_loops):
                if not self.outgoing_queue.full():
                    return True
                await asyncio.sleep(0.1)
            error_time = time.perf_counter()
            logger.error(
                "LDAP write operation was aborted because the backpressure did not decrease within the timeout "
                "message id: %s, time: %s "
                "outgoing_queue length: %s, queue items: %r",
                request.msgid,
                error_time,
                self.outgoing_queue.qsize(),
                list(self.outgoing_queue._queue),
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
        if not await self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_delete(self, request: DELETERequest) -> bytes | str | SockResponse:
        if not await self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_modify(self, request: MODIFYRequest) -> bytes | str | SockResponse:
        if not await self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_modrdn(self, request: MODRDNRequest) -> bytes | str | SockResponse:
        if not await self.request_throttling(request):
            return TIMEOUT_RESPONSE
        return CONTINUE_RESPONSE

    async def do_result(self, request: RESULTRequest) -> bytes | str | SockResponse:
        if self._ignore_result(request):
            return ""

        if request.code != 0:
            logger.warning(
                "Ignoring RESULT response with code %r. msgid: %r info: %r",
                request.code,
                request.msgid,
                request.info if hasattr(request, "info") else "n/a",
            )
            logger.debug("%r", request.__dict__)
            self.legacy_release_backpressure(request.msgid)
            return ""

        ldap_message = self._result_extract_ldap_message(request)

        # Write LDAP transaction to journal
        logger.debug("Writing %r request on DN %r to internal journal.", ldap_message.request_type, request.dn)
        with self.journal_key_mutex:
            # TODO: Write the `ldap_message` into the sqlite journal!
            # sqlite.put(key=self.journal_key, value=ldap_message)
            self.journal_key += 1

        try:
            await asyncio.wait_for(self.outgoing_queue.put(ldap_message), self.backpressure_wait_timeout)
        except asyncio.TimeoutError:
            logger.error("Timeout putting message into outgoing_queue.")
            raise

        self.legacy_release_backpressure(request.msgid)
        return ""

    def _ignore_result(self, request: RESULTRequest) -> bool:
        # Ignore results from read requests
        if getattr(request, "dn", None) is None:
            # A search result or anything where RESULTRequest._parse_ldif didn't find anything.
            return True

        if self.is_refint_request(request._req_lines) and request.msgid == 0:
            logger.debug("Ignoring referential integrity modify result.")
            return True

        # ignore temporary dn modify results (if configured)
        if self.ignore_temporary and self.filter_temporary_dn(request):
            logger.debug("Ignoring temporary object %r.", request.dn)
            return True

        return False

    def _result_request_type(self, request: RESULTRequest) -> RequestType:
        # Parse result request type
        if request.parsed_ldif:
            if isinstance(request.parsed_ldif, list):
                return RequestType.modify
            elif b"newrdn" in request.parsed_ldif:
                return RequestType.modrdn
            else:
                return RequestType.add
        elif request.parsed_ldif is None:
            return RequestType.delete
        else:
            raise ValueError(f"Could not parse the request type of message {request.msgid!r}: {request.parsed_ldif!r}")

    def _result_extract_ldap_message(self, request: RESULTRequest) -> LDAPMessage:
        reqtype = self._result_request_type(request)
        logger.debug("reqtype: %r | parsed_ldif: %r", reqtype, request.parsed_ldif)

        logger.debug("binddn: %r | ctrls: %r", request.binddn, request.ctrls)
        encoded_ctrls = [
            (control_type, criticality, a2b_base64(control_value))
            for (control_type, criticality, control_value) in request.ctrls
        ]
        ctrls = decode_response_ctrls(encoded_ctrls)

        old = None
        new = None
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

        return LDAPMessage(reqtype, request.binddn, request.msgid, request_id.get(), old, new)

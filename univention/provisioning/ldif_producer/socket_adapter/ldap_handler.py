#!/usr/bin/env -S python3 -O
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


from binascii import a2b_base64
from enum import Enum
import logging
from queue import Empty, Full, Queue
import time
from typing import NamedTuple

from ldap0.typehints import EntryMixed
from slapdsock.handler import SlapdSockHandler
from slapdsock.message import CONTINUE_RESPONSE, RESULTRequest
from ldap0.res import decode_response_ctrls
from ldap0.controls.readentry import PostReadControl, PreReadControl
from slapdsock.service import threading

# from slapdsock.service import threading


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


class ReasonableSlapdSockHandler(SlapdSockHandler):
    def __call__(self, *args, **kwargs):
        """
        Handle a request.

        See https://stackoverflow.com/questions/21631799/how-can-i-pass-parameters-to-a-requesthandler
        """
        super().__init__(*args, **kwargs)


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
        outgoing_queue: Queue,
    ):
        self.journal_key = 0
        self.journal_key_mutex = threading.Lock()

        # NOTE: Be careful when extending the Queue maxsize!
        # It's not clear that RESULT responses come in the same order as the
        # requests, so in do_result the timestamps need to be matched with (msgid, connid).
        # Also then several paralel threads may run do_result, so that may need
        # to be somehow serialized to maintain order of ops towards NATS.
        # NOTE: (msgid, connid) are recycled after slapd restart (connid seems
        # to start at 1000 again).
        self.outgoing_queue = outgoing_queue
        self.backpressure_queue = Queue(maxsize=1)
        # self.do_result_lock = threading.Lock()
        self.ignore_temporary = ignore_temporary
        if ignore_temporary:
            temporary_dn_string = ",cn=temporary,cn=univention,"
            self.len_temporary_dn_suffix = len(temporary_dn_string) + len(ldap_base)

    # TODO: Better name to signify that this evaluates ignore_temporaty: apply_temporary_dn_rules() mabe
    def is_temporary_dn(self, request):
        return "," in request.dn[self.len_temporary_dn_suffix :] if self.ignore_temporary else False

    def do_add(self, request):
        """
        ADD
        """
        if self.is_temporary_dn(request):
            return CONTINUE_RESPONSE
        self._log(logging.DEBUG, "do_add = %s", request)
        try:
            # TODO: tune timeout
            self.backpressure_queue.put((request.connid, request.msgid, time.perf_counter()), timeout=2)
        except Full:
            self._log(
                logging.ERROR,
                "do_add = %s failed because no LDAPHandler seat was available within the timeout",
                request,
            )
            return ""
        self._log(
            logging.DEBUG, "added new element to backpressure_queue. new size: %s", self.backpressure_queue.qsize()
        )
        return CONTINUE_RESPONSE

    def do_bind(self, request):
        """
        BIND
        """
        self._log(logging.DEBUG, "do_bind = %s", request)
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
        if self.is_temporary_dn(request):
            return CONTINUE_RESPONSE
        self._log(logging.DEBUG, "do_delete = %s", request)
        try:
            # TODO: tune timeout
            self.backpressure_queue.put((request.connid, request.msgid, time.perf_counter()), timeout=2)
        except Full:
            self._log(
                logging.ERROR,
                "do_add = %s failed because no LDAPHandler seat was available within the timeout",
                request,
            )
            return ""
        self._log(
            logging.DEBUG, "added new element to backpressure_queue. new size: %s", self.backpressure_queue.qsize()
        )
        return CONTINUE_RESPONSE

    def do_modify(self, request):
        """
        MODIFY
        """
        if self.is_temporary_dn(request):
            return CONTINUE_RESPONSE
        self._log(logging.DEBUG, "do_modify = %s", request)
        try:
            # TODO: tune timeout
            self.backpressure_queue.put((request.connid, request.msgid, time.perf_counter()), timeout=2)
        except Full:
            self._log(
                logging.ERROR,
                "do_add = %s failed because no LDAPHandler seat was available within the timeout",
                request,
            )
            return ""
        self._log(
            logging.DEBUG, "added new element to backpressure_queue. new size: %s", self.backpressure_queue.qsize()
        )
        return CONTINUE_RESPONSE

    def do_modrdn(self, request):
        """
        MODRDN
        """
        if self.is_temporary_dn(request):
            return CONTINUE_RESPONSE
        self._log(logging.DEBUG, "do_modrdn = %s", request)
        try:
            # TODO: tune timeout
            self.backpressure_queue.put((request.connid, request.msgid, time.perf_counter()), timeout=2)
        except Full:
            self._log(
                logging.ERROR,
                "do_add = %s failed because no LDAPHandler seat was available within the timeout",
                request,
            )
            return ""
        self._log(
            logging.DEBUG, "added new element to backpressure_queue. new size: %s", self.backpressure_queue.qsize()
        )
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

    # TODO: remove failed attempt
    # def dont_do_result(self, request: RESULTRequest):
    #     """
    #     RESULT
    #     """
    #     self._log(logging.DEBUG, "aquiring the do_resutl lock")
    #     # TODO: timeout is just for development purposes
    #     self.do_result_lock.acquire(timeout=10)
    #     try:
    #         self._do_result(request)
    #     except Exception:
    #         # TODO: Refine this behaviour
    #         self._log(logging.DEBUG, "releasing the do_resutl lock")
    #         self.do_result_lock.release()
    #         (connid, msgid, request_time) = self.backpressure_queue.get()  # signal one seat is free
    #         raise
    #
    #     self._log(logging.DEBUG, "releasing the do_result lock")
    #     self.do_result_lock.release()
    #     (connid, msgid, request_time) = self.backpressure_queue.get()

    def do_result(self, request: RESULTRequest):
        _ = (self, request)  # pylint dummy
        if getattr(request, "dn", None) is None:
            # A search result or anything where RESULTRequest._parse_ldif didn't find anything.
            return ""
        self._log(logging.DEBUG, "do_result = %s", request)
        if self.is_temporary_dn(request):
            self._log(logging.INFO, "ignoring dn = %s", request.dn)
            return ""

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
            self._log(logging.INFO, "binddn = %s", request.binddn)
            self._log(logging.DEBUG, "ctrls = %s", request.ctrls)
            ctrls = [
                (control_type, criticality, a2b_base64(control_value))
                for (control_type, criticality, control_value) in request.ctrls
            ]
            ctrls = decode_response_ctrls(ctrls)

            old = None
            new = None
            for ctrl in ctrls:
                if isinstance(ctrl, PostReadControl):
                    old = ctrl.res.entry_as
                    self._log(logging.INFO, "PostRead entry_as = %s", ctrl.res.entry_as)
                elif isinstance(ctrl, PreReadControl):
                    new = ctrl.res.entry_as
                    self._log(logging.INFO, "PreRead entry_as = %s", ctrl.res.entry_as)

            self._log(
                logging.INFO,
                "Call NATS for %s operation on dn = %s" % (reqtype, request.dn),
            )

            ldap_message = LDAPMessage(reqtype, request.binddn, old, new)

            with self.journal_key_mutex:
                # TODO: Write the `ldap_message` into the sqlite journal!
                # sqlite.put(key=self.journal_key, value=ldap_message)
                self.journal_key += 1

            # TODO: don't know if this shoud stay in
            self.outgoing_queue.put(ldap_message, timeout=5)

        else:
            self._log(logging.INFO, "ignoring op with RESULT code = %s", request.code)
        resonse_time = time.perf_counter()
        try:
            (connid, msgid, request_time) = self.backpressure_queue.get(timeout=5)  # signal one seat is free
        except Empty:
            # TODO: improve this and decide if it should stay in the codebase.
            self._log(logging.ERROR, "no in flight request found in backpressure_queue")
            raise
        self._log(logging.INFO, "processing time  = %s", round(resonse_time - request_time, 6))
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

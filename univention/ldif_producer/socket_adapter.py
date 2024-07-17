# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import threading
from queue import Empty
from socketserver import ThreadingMixIn

from slapdsock.service import SlapdSockServer

from .socket_port import LDIFProducerSocketPort


class LdifProducerSlapdSockServer(SlapdSockServer, LDIFProducerSocketPort):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exit = threading.Event()

    def serve_forever(self):
        # set up the threadpool
        threads = []
        for _ in range(self.thread_pool_size):
            req_thread = threading.Thread(target=self.process_request_thread)
            threads.append(req_thread)
            req_thread.start()
        # server main loop
        while not self.exit.is_set():
            self.handle_request()

        self.logger.info("received exit signal, joining worker threads")
        for req_thread in threads:
            req_thread.join()
        self.logger.info("all worker threads have completed, returning to main thread")

    def process_request_thread(self):
        """
        obtain request from queue instead of directly from server socket
        """
        while not self.exit.is_set():
            try:
                threads = self.requests.get(timeout=1)
            except Empty:
                continue
            self.req_threads_active = len(threads)
            # TODO: I don't understand this!
            if self.req_threads_active > self.req_threads_max:
                self.req_threads_max = self.req_threads_active
            ThreadingMixIn.process_request_thread(self, *threads)

        self.logger.info("exiting worker thread")

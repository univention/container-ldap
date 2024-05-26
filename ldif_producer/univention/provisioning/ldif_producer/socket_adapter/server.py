# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

# import socket
import threading

from abc import ABC, abstractmethod

from socketserver import ThreadingMixIn
from typing import Any, Callable
from slapdsock.service import SlapdSockServer


class LDIFProducerSocketPort(ABC):
    @abstractmethod
    def __init__(
        self,
        server_address: str,
        handler_class: Callable,
        logger: Any,
        average_count: int,
        socket_timeout: int,
        socket_permissions: str,
        allowed_uids: tuple[int, ...],
        allowed_gids: tuple[int, ...],
        thread_pool_size: int,
    ) -> None:
        pass

    @abstractmethod
    def serve_forever(self) -> None:
        pass

    def __enter__(self) -> "LDIFProducerSocketPort":
        return self

    def __exit__(self, *args) -> None:
        pass


class LdifProducerSlapdSockServer(SlapdSockServer, LDIFProducerSocketPort):
    def serve_forever(self):
        # set up the threadpool
        # TODO: listen for sigterm and sigint or provide some option to gracefully terminate all threads.
        for _ in range(self.thread_pool_size):
            req_thread = threading.Thread(target=self.process_request_thread)
            # TODO: daemon should be False, because we need to make sure the thead finishes.
            req_thread.daemon = True
            req_thread.start()
        # server main loop
        while True:
            self.handle_request()
        # TODO: make this actually reachable
        self.server_close()

    def process_request_thread(self):
        """
        obtain request from queue instead of directly from server socket
        """
        while True:
            threads = self.incoming_queue.get()
            self.req_threads_active = len(threads)
            # TODO: Wtf is this doing here?
            if self.req_threads_active > self.req_threads_max:
                self.req_threads_max = self.req_threads_active
            ThreadingMixIn.process_request_thread(self, *threads)

    # TODO: I probably don't have to touch this method. It's here as a reminder for the Moment
    # def handle_request(self):
    #     """
    #     simply collect requests and put them on the queue for the workers.
    #     """
    #     try:
    #         request, client_address = self.get_request()
    #     except socket.error:
    #         return
    #     if self.verify_request(request, client_address):
    #         self.logger.debug('Queuing new request: %r %r', request, client_address)
    #         self.requests.put((request, client_address))

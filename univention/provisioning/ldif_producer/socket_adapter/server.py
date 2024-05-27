# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

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
        self.close = False

        # set up the threadpool
        # TODO: listen for sigterm and sigint or provide some option to gracefully terminate all threads.
        threads = []
        for _ in range(self.thread_pool_size):
            req_thread = threading.Thread(target=self.process_request_thread)
            # TODO: Daemon should be False, because we need to make sure the thread finishes.
            threads.append(req_thread)
            req_thread.start()
        # server main loop
        while True:
            if self.close:
                break
            self.handle_request()

        for req_thread in threads:
            req_thread.join()

        # TODO: make this actually reachable

    def process_request_thread(self):
        """
        obtain request from queue instead of directly from server socket
        """
        while True:
            threads = self.requests.get()
            self.req_threads_active = len(threads)
            # TODO: I don't understand this!
            if self.req_threads_active > self.req_threads_max:
                self.req_threads_max = self.req_threads_active
            ThreadingMixIn.process_request_thread(self, *threads)

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import threading

from abc import ABC, abstractmethod

from typing import Any, Callable


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
        self.exit: threading.Event

    @abstractmethod
    def serve_forever(self) -> None:
        pass

    @abstractmethod
    def server_close(self) -> None:
        pass

    def __enter__(self) -> "LDIFProducerSocketPort":
        return self

    def __exit__(self, *args) -> None:
        pass

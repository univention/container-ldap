# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from univention.provisioning.models import Message

from .config import LDIFProducerSettings

logger = logging.getLogger(__name__)


class LDIFProducerMQPort(ABC):
    @abstractmethod
    def __init__(self, settings: LDIFProducerSettings) -> None:
        self.settings = settings

    @abstractmethod
    async def __aenter__(self) -> "LDIFProducerMQPort":
        pass

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        pass

    @abstractmethod
    async def add_message(self, stream: str, subject: str, message: Message) -> None:
        pass

    @abstractmethod
    async def ensure_stream(self, stream: str, manual_delete: bool, subjects: Optional[List[str]] = None) -> None:
        pass

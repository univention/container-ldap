# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from univention.provisioning.ldif_producer.config import LDIFProducerSettings
from univention.provisioning.models import Message

logger = logging.getLogger(__name__)


class LDIFProducerMQPort(ABC):
    @abstractmethod
    def __init__(self, settings: LDIFProducerSettings) -> None:
        pass

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
    async def ensure_stream(self, stream: str, subjects: Optional[List[str]] = None) -> None:
        pass

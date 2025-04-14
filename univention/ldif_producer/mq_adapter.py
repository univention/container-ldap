# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

import logging
from typing import Any, Callable, List, Optional

import msgpack

from univention.provisioning.models import Message

from .config import LDIFProducerSettings
from .mq_port import LDIFProducerMQPort
from .nats_service import NatsKeys, NatsMQService

logger = logging.getLogger(__name__)


def messagepack_encoder(data: Any) -> bytes:
    return msgpack.packb(data)


class LDIFProducerMQAdapter(LDIFProducerMQPort):
    def __init__(self, settings: LDIFProducerSettings):
        super().__init__(settings)
        self.mq_service = NatsMQService()

    async def __aenter__(self):
        await self.mq_service.connect(
            self.settings.nats_server,
            self.settings.nats_user,
            self.settings.nats_password,
            max_reconnect_attempts=self.settings.nats_max_reconnect_attempts,
        )
        return self

    async def __aexit__(self, *args):
        await self.mq_service.close()

    async def add_message(
        self,
        stream: str,
        subject: str,
        message: Message,
        binary_encoder: Callable[[Any], bytes] = messagepack_encoder,
    ):
        """Publish a message to a NATS subject."""
        stream_name = NatsKeys.stream(stream)

        await self.mq_service._js.publish(
            subject,
            binary_encoder(message.model_dump()),
            stream=stream_name,
        )
        logger.debug(
            "Message was published to the stream: %s with the subject: %s",
            stream_name,
            subject,
        )

    async def ensure_stream(self, stream: str, manual_delete: bool, subjects: Optional[List[str]] = None):
        await self.mq_service.ensure_stream(stream, manual_delete, subjects)

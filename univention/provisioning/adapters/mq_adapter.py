# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
from typing import Any, Callable, List, Optional

import msgpack
from univention.provisioning.models import Message

from univention.provisioning.nats_service import NatsKeys, NatsMQService
from univention.provisioning.ldif_producer.config import LDIFProducerSettings
from univention.provisioning.ports.mq_port import LDIFProducerMQPort


logger = logging.getLogger(__name__)


def messagepack_encoder(data: Any) -> bytes:
    return msgpack.packb(data)


class LDIFProducerMQAdapter(LDIFProducerMQPort):
    def __init__(self, settings: LDIFProducerSettings):
        self.settings = settings
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
        logger.info(
            "Message was published to the stream: %s with the subject: %s",
            stream_name,
            subject,
        )

    async def ensure_stream(self, stream: str, subjects: Optional[List[str]] = None):
        await self.mq_service.ensure_stream(stream, subjects)

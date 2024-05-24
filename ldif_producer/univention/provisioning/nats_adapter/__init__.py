# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
from typing import List, Optional

from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig
from nats.js.errors import (
    NotFoundError,
)

MAX_RECONNECT_ATTEMPTS = 5

logger = logging.getLogger(__name__)


class NatsKeys:
    """A list of keys used in Nats for queueing messages."""

    @staticmethod
    def stream(subject: str) -> str:
        return f"stream:{subject}"

    @staticmethod
    def durable_name(subject: str) -> str:
        return f"durable_name:{subject}"


class NatsMQService:
    def __init__(self):
        self._nats = NATS()
        self._js = self._nats.jetstream()
        self.logger = logging.getLogger(__name__)
        self._message_queue = asyncio.Queue()

    async def connect(self, server: str, user: str, password: str, max_reconnect_attempts=5, **kwargs):
        """Connect to the NATS server.

        Arguments are passed directly to the NATS client.
        https://nats-io.github.io/nats.py/modules.html#asyncio-client

        by default it fails after a maximum of 10 seconds because of a 2 second connect timout * 5 reconnect attempts.
        """
        await self._nats.connect(
            servers=server,
            user=user,
            password=password,
            max_reconnect_attempts=max_reconnect_attempts,
            **kwargs,
        )

    async def close(self):
        await self._nats.close()

    async def initialize_subscription(self, stream: str, subject: str, durable_name: str) -> None:
        """Initializes a stream for a pull consumer, pull consumers can't define a deliver subject"""
        await self.ensure_stream(stream, [subject])
        await self.ensure_consumer(stream)

        durable_name = NatsKeys.durable_name(durable_name)
        stream_name = NatsKeys.stream(stream)
        self.pull_subscription = await self._js.pull_subscribe(
            subject=subject,
            durable=durable_name,
            stream=stream_name,
        )

    async def ensure_stream(self, stream: str, subjects: Optional[List[str]] = None):
        stream_name = NatsKeys.stream(stream)
        try:
            await self._js.stream_info(stream_name)
            self.logger.info("A stream with the name '%s' already exists", stream_name)
        except NotFoundError:
            await self._js.add_stream(name=stream_name, subjects=subjects or [stream])
            self.logger.info("A stream with the name '%s' was created", stream_name)

    async def ensure_consumer(self, stream: str, deliver_subject: Optional[str] = None):
        stream_name = NatsKeys.stream(stream)
        durable_name = NatsKeys.durable_name(stream)

        try:
            await self._js.consumer_info(stream_name, durable_name)
            self.logger.info("A consumer with the name '%s' already exists", durable_name)
        except NotFoundError:
            await self._js.add_consumer(
                stream_name,
                ConsumerConfig(
                    durable_name=durable_name,
                    deliver_subject=deliver_subject,
                    max_ack_pending=1,
                ),
            )
            self.logger.info("A consumer with the name '%s' was created", durable_name)

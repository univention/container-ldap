# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
from datetime import datetime

from slapdsock.log import request_id
from univention.provisioning.models import Message, PublisherName
from univention.provisioning.models.queue import LDIF_STREAM, LDIF_SUBJECT

from .models import LDAPMessage
from .mq_port import LDIFProducerMQPort

logger = logging.getLogger(__name__)


class NATSController:
    def __init__(
        self,
        queue: asyncio.Queue,
        message_queue_port: LDIFProducerMQPort,
    ) -> None:
        self.message_queue_port = message_queue_port

        self.queue = queue

    async def setup(self) -> None:
        await self.message_queue_port.ensure_stream(LDIF_STREAM, [LDIF_SUBJECT])

    async def handle_ldap_message(self, ldap_message: LDAPMessage):
        message = Message(
            publisher_name=PublisherName.ldif_producer,
            ts=datetime.now(),
            realm="ldap",
            topic="ldap",
            body={
                "ldap_request_type": ldap_message.request_type,
                "binddn": ldap_message.binddn,
                "new": ldap_message.new,
                "old": ldap_message.old,
                "message_id": ldap_message.message_id,
                "request_id": ldap_message.request_id,
            },
        )
        if ldap_message.old:
            dn = ldap_message.old["entryDN"][0].decode()
        elif ldap_message.new:
            dn = ldap_message.new["entryDN"][0].decode()
        else:
            dn = "n/a"
        logger.info("Enqueuing message at NATS: %s %r", ldap_message.request_type.value, dn)
        await self.message_queue_port.add_message(LDIF_STREAM, LDIF_SUBJECT, message)

    async def process_queue_forever(self):
        logger.info("Starting to process the outgoing queue.")
        try:
            while True:
                message = await self.queue.get()
                logger.debug("Received a new outgoing message: %r", message)
                await self.handle_ldap_message(message)
        except asyncio.CancelledError:
            logger.info("Stopped handling the outgoing queue.")


async def run_mq_sender(
    message_queue_port: LDIFProducerMQPort,
    outgoing_queue: asyncio.Queue,
):
    """Start a sending messages found in `outgoing_queue`. Will only return when canceled."""
    request_id.set("mq-sender")
    async with message_queue_port:
        nats_controller = NATSController(outgoing_queue, message_queue_port)
        await nats_controller.setup()
        logger.info("Starting to send messages to NATS at %r.", message_queue_port.settings.nats_server)
        try:
            await nats_controller.process_queue_forever()
        except asyncio.CancelledError:
            logger.info("Stopped sending messages to NATS at %r.", message_queue_port.settings.nats_server)

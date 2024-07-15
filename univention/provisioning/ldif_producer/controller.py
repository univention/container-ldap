# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
from datetime import datetime
import logging
from pathlib import Path
import sys
from typing import Awaitable, Callable


from univention.provisioning.models.queue import LDIF_STREAM, LDIF_SUBJECT

from univention.provisioning.adapters.mq_adapter import LDIFProducerMQAdapter
from univention.provisioning.models import Message, PublisherName
from univention.provisioning.ports.mq_port import LDIFProducerMQPort

from config import LDIFProducerSettings, get_ldif_producer_settings
from ldap_handler import LDAPHandler, LDAPMessage


logger = logging.getLogger(__name__)
AsyncioHandler = Callable[[asyncio.StreamReader, asyncio.StreamWriter], Awaitable[None]]


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
            logger.info("Shutting down queue handling.")


def setup_logging():
    # TODO: with Python 3.12 consider adding '[%(taskname)d]' to log the name of the current asyncio.Task
    log_formatter = logging.Formatter("%(asctime)s %(levelname)s [%(module)s.%(funcName)s:%(lineno)s] %(message)s")
    # stderr: unbuffered to prevent BrokenPipe in asyncio.Cancel during shutdown
    stdout_handler = logging.StreamHandler(sys.stderr)
    stdout_handler.setFormatter(log_formatter)
    stdout_handler.setLevel(logging.DEBUG)
    _logger = logging.getLogger()
    _logger.addHandler(stdout_handler)
    _logger.setLevel(logging.DEBUG)


async def start_mq_sender(
    message_queue_port_type: type[LDIFProducerMQPort],
    settings: LDIFProducerSettings,
    outgoing_queue: asyncio.Queue,
):
    async with message_queue_port_type(settings) as message_queue_port:
        nats_controller = NATSController(outgoing_queue, message_queue_port)
        await nats_controller.setup()

        try:
            await nats_controller.process_queue_forever()
        except asyncio.CancelledError:
            logger.info("Stopped sending messages to NATS")


async def start_socket_server(socket_path: Path, handler: AsyncioHandler):
    socket_path.unlink(missing_ok=True)
    server = await asyncio.start_unix_server(handler, path=socket_path)
    logger.info("Starting to listen on socket '%s'...", socket_path)
    async with server:
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            pass
    logger.info("Stopped listening on socket")


async def main():
    # setup
    setup_logging()
    settings = get_ldif_producer_settings()
    socket_path = Path(settings.socket_file_location)
    outgoing_queue = asyncio.Queue(maxsize=settings.max_in_flight_ldap_messages)
    # start message sender task in the background
    sender_coro = start_mq_sender(LDIFProducerMQAdapter, settings, outgoing_queue)
    sender_task = asyncio.create_task(sender_coro)
    await asyncio.sleep(0)
    logger.info("Started MQ sender task.")
    # start socket listener in the foreground
    handler = LDAPHandler(
        ldap_base=settings.ldap_base_dn,
        ldap_threads=settings.ldap_threads,
        ignore_temporary=settings.ignore_temporary_objects,
        outgoing_queue=outgoing_queue,
        backpressure_wait_timeout=settings.backpressure_wait_timeout,
    )
    await start_socket_server(socket_path, handler.handle)
    # shutdown
    sender_task.cancel("Shutdown")


if __name__ == "__main__":
    asyncio.run(main())

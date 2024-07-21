#!/usr/bin/env -S python3 -O
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import signal
import sys
from importlib.metadata import version
from typing import Awaitable, Callable

from slapdsock.handler import SlapdSockHandler
from slapdsock.log import RequestIdFilter, request_id
from slapdsock.server import serve_forever
from univention.ldif_producer.message_queue_sender import MessageQueueSender
from univention.ldif_producer.mq_port import LDIFProducerMQPort
from univention.ldif_producer.nats_service import MessageQueueConnectionError

from .config import LDIFProducerSettings, get_ldif_producer_settings
from .ldap_reciever import LDAPReciever
from .mq_adapter import LDIFProducerMQAdapter

AsyncioHandler = Callable[[asyncio.StreamReader, asyncio.StreamWriter], Awaitable[None]]
logger = logging.getLogger(__name__)


def setup_logging() -> None:
    fmt = "%(asctime)s %(levelname)-8s [%(request_id)-10s][%(module)s.%(funcName)s:%(lineno)s] %(message)s"
    log_formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler(sys.stderr)  # unbuffered to prevent BrokenPipe in asyncio.Cancel during shutdown
    request_id_filter = RequestIdFilter()
    handler.addFilter(request_id_filter)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.DEBUG)
    _logger = logging.getLogger()
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)


async def run_message_queue_sender(message_queue_sender: MessageQueueSender):
    """Start a sending messages found in `outgoing_queue`. Will only return when canceled."""
    request_id.set("mq-sender")

    logger.info("Starting to send messages to NATS.")
    try:
        await message_queue_sender.process_queue_forever()
    except asyncio.CancelledError:
        logger.info("Stopped sending messages to NATS")


def shutdown_signal_handler(signum, frame) -> None:
    logger.info("Received signal %s (%d). Shutting down.", signal.Signals(signum).name, signum)
    sys.exit(0)


def install_signal_handlers() -> None:
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown_signal_handler)


async def run(
    settings: LDIFProducerSettings,
    ldap_reciever_type: type[LDAPReciever],
    slapd_sock_handler_type: type[SlapdSockHandler],
    message_queue_port_type: type[LDIFProducerMQPort],
) -> None:
    # setup

    outgoing_queue = asyncio.Queue(maxsize=settings.max_in_flight_ldap_messages)

    ldap_reciever = ldap_reciever_type(
        ldap_base=settings.ldap_base_dn,
        ignore_temporary=settings.ignore_temporary_objects,
        outgoing_queue=outgoing_queue,
        backpressure_wait_timeout=settings.backpressure_wait_timeout,
    )
    handler = slapd_sock_handler_type(ldap_reciever)

    try:
        async with message_queue_port_type(settings) as message_queue_port:
            message_queue_sender = MessageQueueSender(outgoing_queue, message_queue_port)
            await message_queue_sender.setup()

            # start message sender task in the background
            sender_task = asyncio.create_task(run_message_queue_sender(message_queue_sender), name="mq_sender")
            await asyncio.sleep(0)
            logger.info("Started MQ sender task in the background.")

            # start socket listener in the foreground
            await serve_forever(settings.socket_file_location, handler.handle)
            # foreground task returned, shutdown background task
            sender_task.cancel("Shutdown")
            await sender_task
    except MessageQueueConnectionError:
        logger.error("NATS message queue connection failed. Shutting down the ldif-producer")


def main() -> None:
    request_id.set("main")
    setup_logging()
    install_signal_handlers()
    logger.info("Starting LDIF-Producer version %s.", version("nubus-ldif-producer"))
    asyncio.run(
        run(
            get_ldif_producer_settings(),
            LDAPReciever,
            SlapdSockHandler,
            LDIFProducerMQAdapter,
        )
    )


if __name__ == "__main__":
    main()

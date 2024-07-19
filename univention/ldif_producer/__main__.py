#!/usr/bin/env -S python3 -O
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import signal
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Awaitable, Callable

from slapdsock.log import RequestIdFilter, request_id
from slapdsock.server import serve_forever

from .config import get_ldif_producer_settings
from .ldap_reciever import LDAPReciever
from .message_queue_sender import run_message_queue_sender
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


async def main() -> None:
    # setup
    settings = get_ldif_producer_settings()
    socket_path = Path(settings.socket_file_location)
    outgoing_queue = asyncio.Queue(maxsize=settings.max_in_flight_ldap_messages)
    # start message sender task in the background
    sender_coro = run_message_queue_sender(LDIFProducerMQAdapter(settings), outgoing_queue)
    sender_task = asyncio.create_task(sender_coro, name="mq_sender")
    await asyncio.sleep(0)
    logger.info("Started MQ sender task in the background.")
    # start socket listener in the foreground
    handler = LDAPReciever(
        ldap_base=settings.ldap_base_dn,
        ignore_temporary=settings.ignore_temporary_objects,
        outgoing_queue=outgoing_queue,
        backpressure_wait_timeout=settings.backpressure_wait_timeout,
    )
    await serve_forever(socket_path, handler.handle)
    # foreground task returned, shutdown background task
    sender_task.cancel("Shutdown")
    await sender_task


def shutdown_signal_handler(signum, frame) -> None:
    logger.info("Received signal %s (%d). Shutting down.", signal.Signals(signum).name, signum)
    sys.exit(0)


def install_signal_handlers() -> None:
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown_signal_handler)


if __name__ == "__main__":
    request_id.set("main")
    setup_logging()
    install_signal_handlers()
    logger.info("Starting LDIF-Producer version %s.", version("nubus-ldif-producer"))
    asyncio.run(main())

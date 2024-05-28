# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import signal
import sys
from queue import Empty, Queue

from datetime import datetime
import threading

from univention.provisioning.ldif_producer.config import LDIFProducerSettings, get_ldif_producer_settings
from univention.provisioning.ldif_producer.port import (
    LDAP_STREAM,
    LDAP_SUBJECT,
    LDIFProducerAdapter,
    LDIFProducerMQPort,
)
from univention.provisioning.ldif_producer.socket_adapter.ldap_handler import LDAPHandler, LDAPMessage
from univention.provisioning.models import Message, PublisherName

from univention.provisioning.ldif_producer.socket_adapter.server import (
    LDIFProducerSocketPort,
    LdifProducerSlapdSockServer,
)


class NATSController:
    def __init__(
        self,
        queue: Queue,
        message_queue_port: LDIFProducerMQPort,
    ) -> None:
        self.message_queue_port = message_queue_port

        self.queue = queue
        self.logger = logging.getLogger(__name__)

    async def setup(self) -> None:
        await self.message_queue_port.ensure_stream(LDAP_STREAM, [LDAP_SUBJECT])

    async def handle_ldap_message(self, ldap_message: LDAPMessage):
        self.logger.info(
            "sending LDAP message to NATS request_type: %s binddn: %s", ldap_message.request_type, ldap_message.binddn
        )
        message = Message(
            publisher_name=PublisherName.udm_listener,
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
        await self.message_queue_port.add_message(LDAP_STREAM, LDAP_SUBJECT, message)

    async def process_queue_forever(self):
        self.logger.info("starting to process the outgoing queue")
        while True:
            try:
                message = self.queue.get(timeout=1)
            except Empty:
                # give the signal handler a chance to interrupt the event loop
                await asyncio.sleep(0.0001)
                continue
            self.logger.debug("received a new outgoing message")
            await self.handle_ldap_message(message)


async def signal_handler(signal: signal.Signals, logger: logging.Logger, socket_port: LDIFProducerSocketPort):
    logger.info("recieved stop signal: %s", signal)

    logger.info("closing the unix socket and shutting down the socket server")
    socket_port.server_close()
    socket_port.exit.set()

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("collected all asyncio tasks")

    asyncio.get_event_loop().stop()


def get_logger():
    logger = logging.getLogger(__name__)
    stdout_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(process)d %(thread)d] [%(levelname)s] %(message)s [%(threadName)s]"
    )
    stdout_handler.setFormatter(log_formatter)
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)

    return logger


async def run(
    message_queue_port_type: type[LDIFProducerMQPort],
    socket_port_type: type[LDIFProducerSocketPort],
    ldap_handler_type: type[LDAPHandler],
    settings: LDIFProducerSettings,
):
    logger = get_logger()

    outgoing_queue = Queue(settings.max_in_flight_ldap_messages)

    async with message_queue_port_type(settings) as message_queue_port:
        nats_controller = NATSController(outgoing_queue, message_queue_port)
        await nats_controller.setup()

        ldap_handler = ldap_handler_type(
            settings.ldap_base_dn,
            settings.ldap_threads,
            settings.ignore_temporary_objects,
            outgoing_queue,
        )

        socket_port = socket_port_type(
            server_address=settings.socket_file_location,
            handler_class=ldap_handler,
            logger=logger,
            average_count=10,
            socket_timeout=1,
            socket_permissions="600",
            allowed_uids=(0,),
            allowed_gids=(0,),
            thread_pool_size=settings.ldap_threads,
        )

        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            asyncio.get_running_loop().add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(signal_handler(s, logger, socket_port))
            )

        socket_main_thread = threading.Thread(name="socket_main_thread", target=socket_port.serve_forever)
        socket_main_thread.start()

        try:
            await nats_controller.process_queue_forever()
        except asyncio.CancelledError:
            logger.info("Stopped sending messages to NATS")
            socket_main_thread.join()
            pass


def main():
    settings = get_ldif_producer_settings()
    asyncio.run(run(LDIFProducerAdapter, LdifProducerSlapdSockServer, LDAPHandler, settings))


if __name__ == "__main__":
    main()

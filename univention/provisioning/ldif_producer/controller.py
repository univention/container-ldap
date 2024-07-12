# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import signal
import sys
from queue import Empty, Queue

from datetime import datetime
import threading

from univention.provisioning.models.queue import LDIF_STREAM, LDIF_SUBJECT

from univention.provisioning.adapters.mq_adapter import LDIFProducerMQAdapter
from univention.provisioning.adapters.socket_adapter import LdifProducerSlapdSockServer
from univention.provisioning.ldif_producer.config import LDIFProducerSettings, get_ldif_producer_settings
from univention.provisioning.models import Message, PublisherName
from univention.provisioning.ports.mq_port import LDIFProducerMQPort
from univention.provisioning.ports.socket_port import LDIFProducerSocketPort
from univention.provisioning.ldif_producer.ldap_handler import LDAPHandler, LDAPMessage


logger = logging.getLogger(__name__)


class NATSController:
    def __init__(
        self,
        queue: Queue,
        message_queue_port: LDIFProducerMQPort,
    ) -> None:
        self.message_queue_port = message_queue_port

        self.queue = queue

    async def setup(self) -> None:
        await self.message_queue_port.ensure_stream(LDIF_STREAM, [LDIF_SUBJECT])

    async def handle_ldap_message(self, ldap_message: LDAPMessage):
        logger.info(
            "sending LDAP message to NATS request_type: %s binddn: %s", ldap_message.request_type, ldap_message.binddn
        )
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
        await self.message_queue_port.add_message(LDIF_STREAM, LDIF_SUBJECT, message)

    async def process_queue_forever(self):
        logger.info("starting to process the outgoing queue")
        while True:
            try:
                message = self.queue.get(timeout=1)
            except Empty:
                # give the signal handler a chance to interrupt the event loop
                await asyncio.sleep(0)
                continue
            logger.debug("received a new outgoing message")
            await self.handle_ldap_message(message)


async def signal_handler(signal_: signal.Signals, socket_port: LDIFProducerSocketPort):
    logger.info("received stop signal: %s", signal_)

    logger.info("closing the unix socket and shutting down the socket server")
    socket_port.server_close()
    socket_port.exit.set()

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("collected all asyncio tasks")

    asyncio.get_event_loop().stop()


def setup_logging():
    stdout_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(process)d %(thread)d] [%(levelname)s] %(message)s"
    )
    stdout_handler.setFormatter(log_formatter)
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)


def create_socket_server(socket_port_type: type[LDIFProducerSocketPort], ldap_handler_type: type[LDAPHandler], settings: LDIFProducerSettings, outgoing_queue: Queue) -> LDIFProducerSocketPort:
    ldap_handler = ldap_handler_type(
        ldap_base=settings.ldap_base_dn,
        ldap_threads=settings.ldap_threads,
        ignore_temporary=settings.ignore_temporary_objects,
        outgoing_queue=outgoing_queue,
        backpressure_wait_timeout=settings.backpressure_wait_timeout,
    )
    socket_server = socket_port_type(
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
    return socket_server


async def run_mq_sender(
    message_queue_port_type: type[LDIFProducerMQPort],
    settings: LDIFProducerSettings,
    outgoing_queue: Queue,
    socket_server: LDIFProducerSocketPort,
):
    async with message_queue_port_type(settings) as message_queue_port:
        nats_controller = NATSController(outgoing_queue, message_queue_port)
        await nats_controller.setup()

        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            asyncio.get_running_loop().add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(signal_handler(s, socket_server))
            )

        try:
            await nats_controller.process_queue_forever()
        except asyncio.CancelledError:
            logger.info("Stopped sending messages to NATS")
            pass


def main():
    setup_logging()
    settings = get_ldif_producer_settings()
    outgoing_queue = Queue(maxsize=settings.max_in_flight_ldap_messages)
    # start socket listener
    socket_server = create_socket_server(LdifProducerSlapdSockServer, LDAPHandler, settings, outgoing_queue)
    socket_main_thread = threading.Thread(name="socket_main_thread", target=socket_server.serve_forever)
    socket_main_thread.start()
    # start message sender
    asyncio.run(run_mq_sender(LDIFProducerMQAdapter, settings, outgoing_queue, socket_server))
    # shutdown
    socket_main_thread.join()


if __name__ == "__main__":
    main()

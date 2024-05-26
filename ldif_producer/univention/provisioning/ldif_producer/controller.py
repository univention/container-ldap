# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
from queue import Queue
import sys

from datetime import datetime
import threading

from slapdsock.service import SlapdSockServer

from univention.provisioning.ldif_producer.config import (
    LDIFProducerSettings,
    get_ldif_producer_settings,
)
from univention.provisioning.ldif_producer.port import (
    LDAP_STREAM,
    LDAP_SUBJECT,
    LDIFProducerAdapter,
    LDIFProducerMQPort,
)
from univention.provisioning.ldif_producer.socket_adapter.slapdsocklistener import (
    LDAPHandler,
    LDAPMessage,
)
from univention.provisioning.models import Message, PublisherName

from univention.provisioning.ldif_producer.socket_adapter.server import (
    LDIFProducerSocketPort,
)


class LDIFProducerController:
    def __init__(
        self,
        settings: LDIFProducerSettings,
        message_queue_port: LDIFProducerMQPort,
        socket_port: type[LDIFProducerSocketPort],
    ) -> None:
        self.settings = settings
        self.message_queue_port = message_queue_port
        self.socket_port = socket_port

        self.queue = Queue(self.settings.max_in_flight_ldap_messages)

        self.logger = logging.getLogger(__name__)

        stdout_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(logging.DEBUG)

    async def handle_ldap_message(self, ldap_message: LDAPMessage):
        self.logger.info("handeling ldap message: %s", ldap_message.request_type)
        new = {
            "dn": ldap_message.request.dn,
            "request_type": ldap_message.request_type,
            "ldif": ldap_message.request.parsed_ldif,
        }
        old = None
        message = Message(
            publisher_name=PublisherName.udm_listener,
            ts=datetime.now(),
            realm="ldap",
            topic="ldap",
            body={"new": new, "old": old},
        )
        await self.message_queue_port.add_message(LDAP_STREAM, LDAP_SUBJECT, message)

    async def process_queue(self):
        self.logger.info("starting the processing of the outgoing queue")
        while True:
            message = self.queue.get()
            self.logger.info("received a new outgoing message")
            if message is None:
                break
            await self.handle_ldap_message(message)

    def run_socket(self, handler: LDAPHandler):
        with self.socket_port(
            server_address="/var/lib/univention-ldap/slapd-sock",
            handler_class=handler,
            logger=self.logger,
            average_count=10,
            socket_timeout=30,
            socket_permissions="600",
            allowed_uids=(0,),
            allowed_gids=(0,),
            thread_pool_size=self.settings.ldap_threads,
        ) as slapdsock_server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            self.logger.info("starting slapd socket server")
            slapdsock_server.serve_forever()

    async def run(self):
        await self.message_queue_port.ensure_stream(LDAP_STREAM, [LDAP_SUBJECT])
        ldap_handler = LDAPHandler(
            self.settings.ldap_base_dn,
            self.settings.ldap_threads,
            self.settings.ignore_temporary_objects,
            self.queue,
        )

        socket_main_thread = threading.Thread(name="socket_main_thread", target=self.run_socket, args=(ldap_handler,))
        socket_main_thread.start()

        await self.process_queue()


async def run(
    message_queue_port: type[LDIFProducerMQPort],
    socket_port: type[LDIFProducerSocketPort],
):
    settings = get_ldif_producer_settings()
    async with message_queue_port(settings) as mq_port:
        controller = LDIFProducerController(settings, mq_port, socket_port)
        await controller.run()


def main():
    asyncio.run(run(LDIFProducerAdapter, SlapdSockServer))


if __name__ == "__main__":
    main()

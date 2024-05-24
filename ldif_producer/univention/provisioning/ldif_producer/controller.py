# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import sys

from datetime import datetime

from slapdsock.service import SlapdSockServer

from univention.provisioning.ldif_producer.config import get_ldif_producer_settings
from univention.provisioning.ldif_producer.port import LDAP_STREAM, LDAP_SUBJECT, LDIFProducerAdapter, LDIFProducerPort
from univention.provisioning.ldif_producer.slapdsocklistener import LDAPHandler
from univention.provisioning.models import Message, PublisherName


class LDIFProducerController:
    def __init__(self, message_queue_port: LDIFProducerPort) -> None:
        self.logger = logging.getLogger(__name__)

        stdout_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(logging.DEBUG)

        self.message_queue_port = message_queue_port

    async def _handle_changes(self, new, old):
        message = Message(
            publisher_name=PublisherName.udm_listener,
            ts=datetime.now(),
            realm="ldap",
            topic="ldap",
            body={"new": new, "old": old},
        )
        await self.message_queue_port.add_message(LDAP_STREAM, LDAP_SUBJECT, message)

    def handle_changes(self, new, old):
        asyncio.run(self._handle_changes(new, old))

    async def run(self):
        settings = get_ldif_producer_settings()
        ldap_handler = LDAPHandler(
            settings.ldap_base_dn, settings.ldap_threads, settings.ignore_temporary_objects, self.handle_changes
        )

        with SlapdSockServer(
            server_address="/var/lib/univention-ldap/slapd-sock",
            handler_class=ldap_handler,
            logger=self.logger,
            average_count=10,
            socket_timeout=30,
            socket_permissions="600",
            allowed_uids=(0,),
            allowed_gids=(0,),
            thread_pool_size=settings.ldap_threads,
        ) as slapdsock_server:
            await self.message_queue_port.ensure_stream(LDAP_STREAM, [LDAP_SUBJECT])
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            slapdsock_server.serve_forever()


async def run(ldif_producer_port: type[LDIFProducerPort]):
    settings = get_ldif_producer_settings()
    async with ldif_producer_port(settings) as mq_port:
        controller = LDIFProducerController(mq_port)
        await controller.run()


def main():
    asyncio.run(run(LDIFProducerAdapter))


if __name__ == "__main__":
    main()

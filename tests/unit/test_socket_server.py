# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from queue import Queue
import socket
import time
from unittest import mock

import pytest
from slapdsock.handler import logging
from slapdsock.service import threading

from univention.provisioning.ldif_producer.controller import get_logger
from univention.provisioning.ldif_producer.socket_adapter.server import LdifProducerSlapdSockServer


@pytest.fixture
def logger() -> logging.Logger:
    return get_logger()


@pytest.fixture
def socket_server(logger) -> LdifProducerSlapdSockServer:
    ldap_handler = mock.MagicMock()

    server = LdifProducerSlapdSockServer.__new__(LdifProducerSlapdSockServer)
    server.server_activate = mock.MagicMock()

    server.server_bind = mock.MagicMock()

    server.__init__(
        server_address="/foo/bar/baz",
        handler_class=ldap_handler,
        logger=logger,
        average_count=10,
        socket_timeout=1,
        socket_permissions="600",
        allowed_uids=(0,),
        allowed_gids=(0,),
        thread_pool_size=1,
    )
    server.server_activate.assert_called_once()

    return server


def test_socket_server_initialization(socket_server):
    pass


def test_exit_socket_server(logger: logging.Logger, socket_server: LdifProducerSlapdSockServer):
    socket_main_thread = threading.Thread(name="socket_main_thread", target=socket_server.serve_forever)
    logger.warning("Starting socket server thread")
    socket_main_thread.start()

    logger.warning("Sending exit event to socket server thread")
    socket_server.exit.set()
    logger.warning("Trying to join the socket server thread")
    socket_main_thread.join(timeout=5)
    logger.warning("joined socket thread, exiting")


def test_serve_forever(logger: logging.Logger, socket_server: LdifProducerSlapdSockServer):
    counter = 0
    request_syncronization_queue = Queue()

    def get_request_override():
        nonlocal counter
        counter += 1
        if counter <= 5:
            return (mock.MagicMock(), ("addr", 12345))
        time.sleep(0.5)
        raise socket.error("mocked empty socket timeout error")

    def finish_request_override(request, client_address):
        request_syncronization_queue.put((request, client_address))

    socket_server.verify_request = mock.MagicMock(return_value=True)
    socket_server.get_request = get_request_override
    socket_server.finish_request = finish_request_override

    socket_main_thread = threading.Thread(name="socket_main_thread", target=socket_server.serve_forever)
    socket_main_thread.start()

    for i in range(5):
        request_syncronization_queue.get(timeout=2)
        logger.info("request number %d was processed", i + 1)

    logger.warning("Sending exit event to socket server thread")
    socket_server.exit.set()
    logger.warning("Trying to join the socket server thread")
    socket_main_thread.join(timeout=5)
    logger.warning("joined socket thread, exiting")

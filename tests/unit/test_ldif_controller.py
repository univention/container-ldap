# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
from queue import Queue
import signal
from unittest.mock import ANY, MagicMock, call

import pytest
from univention.provisioning.ldif_producer.controller import NATSController, get_logger, signal_handler
from univention.provisioning.ports.mq_port import LDIFProducerMQPort
from univention.provisioning.adapters.mq_adapter import LDIF_STREAM, LDIF_SUBJECT
from univention.provisioning.ldif_producer.ldap_handler import LDAPMessage, RequestType


@pytest.mark.asyncio
async def test_controller_setup(mock_message_queue_port: LDIFProducerMQPort):
    queue = MagicMock()
    controller = NATSController(
        queue=queue,
        message_queue_port=mock_message_queue_port,
    )

    await controller.setup()

    mock_message_queue_port.ensure_stream.assert_called_once_with(LDIF_STREAM, [LDIF_SUBJECT])


@pytest.mark.asyncio
async def test_nats_controller(mock_message_queue_port: LDIFProducerMQPort):
    queue = Queue(maxsize=20)
    expected_calls = []
    for i in range(10):
        ldap_message = LDAPMessage(
            request_type=RequestType.add,
            binddn=f"foobar: {i}",
            old=None,
            new={"number": i},
        )
        queue.put(ldap_message)
        expected_calls.append(call(LDIF_STREAM, LDIF_SUBJECT, ANY))

    controller = NATSController(
        queue=queue,
        message_queue_port=mock_message_queue_port,
    )

    async def check_queue_and_cancel(task):
        while not queue.empty():
            await asyncio.sleep(0.2)
        task.cancel()

    task = asyncio.create_task(controller.process_queue_forever())
    monitor = asyncio.create_task(check_queue_and_cancel(task))

    with pytest.raises(asyncio.CancelledError):
        await asyncio.gather(monitor, task)
    assert queue.empty()

    mock_message_queue_port.add_message.assert_has_calls(expected_calls, any_order=True)
    assert mock_message_queue_port.add_message.call_count == len(expected_calls)


@pytest.mark.asyncio
async def test_signal_handler():
    logger = get_logger()
    socket_port = MagicMock()

    async def dummy_task():
        while True:
            await asyncio.sleep(1)

    task1 = asyncio.create_task(dummy_task())
    task2 = asyncio.create_task(dummy_task())

    await asyncio.sleep(0)

    signal_handler(signal.SIGINT, MagicMock(), logger, socket_port)

    socket_port.server_close.assert_called_once()
    assert socket_port.exit.is_set()

    with pytest.raises(asyncio.CancelledError):
        await asyncio.gather(task1, task2)

    socket_port.server_close.assert_called_once()
    assert socket_port.exit.is_set()

    assert task1.cancelled()
    assert task2.cancelled()

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
from unittest.mock import ANY, MagicMock, call

import pytest

from univention.ldif_producer.ldap_reciever import LDAPMessage, RequestType
from univention.ldif_producer.message_queue_sender import MessageQueueSender
from univention.ldif_producer.mq_port import LDIFProducerMQPort
from univention.provisioning.models.queue import LDIF_STREAM, LDIF_SUBJECT


@pytest.mark.asyncio
async def test_message_queue_sender_setup(mock_message_queue_port: LDIFProducerMQPort):
    queue = MagicMock()
    message_queue_sender = MessageQueueSender(
        queue=queue,
        message_queue_port=mock_message_queue_port,
    )

    await message_queue_sender.setup()

    mock_message_queue_port.ensure_stream.assert_called_once_with(LDIF_STREAM, [LDIF_SUBJECT])


@pytest.mark.asyncio
async def test_nats_message_queue_sender(mock_message_queue_port: LDIFProducerMQPort):
    queue = asyncio.Queue(maxsize=20)
    expected_calls = []
    for i in range(10):
        ldap_message = LDAPMessage(
            request_type=RequestType.add,
            binddn=f"foobar: {i}",
            message_id=33,
            request_id="foobar",
            old=None,
            new={
                "entryDN": [
                    b"cn=univentionfeedback,cn=entry,cn=portals,cn=univention,dc=univention-organization,dc=intranet"
                ]
            },
        )
        await queue.put(ldap_message)
        expected_calls.append(call(LDIF_STREAM, LDIF_SUBJECT, ANY))

    message_queue_sender = MessageQueueSender(
        queue=queue,
        message_queue_port=mock_message_queue_port,
    )

    async def check_queue_and_cancel(task_):
        while not queue.empty():
            await asyncio.sleep(0.2)
        task_.cancel()

    task = asyncio.create_task(message_queue_sender.process_queue_forever())
    monitor = asyncio.create_task(check_queue_and_cancel(task))

    await asyncio.gather(monitor, task)
    assert queue.empty()

    mock_message_queue_port.add_message.assert_has_calls(expected_calls, any_order=True)
    assert mock_message_queue_port.add_message.call_count == len(expected_calls)


# reactivate once a more complicated signal handler is implemented.
# @pytest.mark.asyncio
# async def test_signal_handler():
#     socket_port = MagicMock()
#
#     async def dummy_task():
#         try:
#             while True:
#                 await asyncio.sleep(1)
#         except asyncio.CancelledError:
#             pass
#
#     task1 = asyncio.create_task(dummy_task())
#     task2 = asyncio.create_task(dummy_task())
#
#     await asyncio.sleep(0)
#
#     await signal_handler(signal.SIGINT, socket_port)
#
#     socket_port.server_close.assert_called_once()
#     assert socket_port.exit.is_set()
#
#     await task1
#     await task2

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

import asyncio

import pytest

from slapdsock.handler import MODIFYRequest
from univention.ldif_producer.ldap_reciever import LDAPReciever


@pytest.fixture
def throttling_outgoing_queue() -> asyncio.Queue:
    return asyncio.Queue(maxsize=1)


@pytest.fixture
def throttling_ldap_reciever(throttling_outgoing_queue: asyncio.Queue) -> LDAPReciever:
    return LDAPReciever(
        "dc=univention-organization,dc=intranet",
        True,
        throttling_outgoing_queue,
        0.1,
    )


@pytest.fixture
def modify_request() -> MODIFYRequest:
    binary_request = b"MODIFY\nmsgid: 0\nbinddn: \npeername: \nconnid: 18446744073709551615\nsuffix: dc=univention-organization,dc=intranet\ndn: cn=Domain Users,cn=groups,dc=univention-organization,dc=intranet\ndelete: uniqueMember\nuniqueMember: uid=0ad4a8be-35f2-11ef-951b-37af858e1364,cn=users,dc=univention-organization,dc=intranet\n-\nreplace: modifiersName\nmodifiersName: cn=Referential Integrity Overlay\n-\n\n"  # noqa E501
    req_lines = binary_request.split(b"\n")
    return MODIFYRequest(req_lines)


@pytest.mark.asyncio
async def test_happpy_path(throttling_ldap_reciever: LDAPReciever, modify_request: MODIFYRequest):
    assert await throttling_ldap_reciever.request_throttling(modify_request)


@pytest.mark.asyncio
async def test_blocking(throttling_ldap_reciever: LDAPReciever, modify_request: MODIFYRequest):
    await throttling_ldap_reciever.outgoing_queue.put("foobar")

    assert not await throttling_ldap_reciever.request_throttling(modify_request)


@pytest.mark.asyncio
async def test_temporary_blocking(throttling_ldap_reciever: LDAPReciever, modify_request: MODIFYRequest):
    throttling_ldap_reciever.backpressure_wait_timeout = 5

    await throttling_ldap_reciever.outgoing_queue.put("foobar")

    request_throttling_task = asyncio.create_task(throttling_ldap_reciever.request_throttling(modify_request))
    await asyncio.sleep(0.3)
    assert await throttling_ldap_reciever.outgoing_queue.get()

    assert await request_throttling_task


@pytest.mark.asyncio
async def test_multiple_temporary_blocking(throttling_ldap_reciever: LDAPReciever, modify_request: MODIFYRequest):
    throttling_ldap_reciever.backpressure_wait_timeout = 5

    await throttling_ldap_reciever.outgoing_queue.put("foobar")

    tasks = []
    for _ in range(3):
        t = asyncio.create_task(throttling_ldap_reciever.request_throttling(modify_request))
        tasks.append(t)
    await asyncio.sleep(0.5)
    assert await throttling_ldap_reciever.outgoing_queue.get()

    for request_throttling_task in tasks:
        assert await request_throttling_task

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

import asyncio
import json
import logging
import struct
import time
from pprint import pprint
from unittest.mock import AsyncMock, MagicMock

import pytest

from slapdsock.handler import SlapdSockHandler
from slapdsock.message import CONTINUE_RESPONSE
from univention.ldif_producer.ldap_reciever import TIMEOUT_RESPONSE, LDAPReciever
from univention.ldif_producer.models import RequestType


def get_test_data(filename: str) -> list[dict]:
    with open(filename, "r") as f:
        request_list = json.load(f)
    for request in request_list:
        request["request_data"] = request["request_data"].encode("UTF-8")
    return request_list


def get_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        "%(asctime)s [%(process)d %(thread)d] [%(levelname)s] %(message)s [%(threadName)s]"
    )
    logger.propagate = False
    handler.setFormatter(log_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


@pytest.fixture
def outgoing_queue() -> asyncio.Queue:
    return asyncio.Queue(-1)


@pytest.fixture
def mock_socket_request():
    request = MagicMock()
    request.sendall = MagicMock()
    sockopt_struct = struct.pack("3i", 1234, 1000, 1000)
    request.getsockopt = MagicMock(return_value=sockopt_struct)

    return request


@pytest.fixture(scope="function")
def ldap_reciever(outgoing_queue, mock_socket_request, request) -> LDAPReciever:
    ignore_temporary = getattr(request, "param", True)
    ldap_reciever = LDAPReciever(
        "dc=univention-organization,dc=intranet",
        ignore_temporary,
        outgoing_queue,
        1,
    )
    return ldap_reciever


@pytest.fixture(scope="function")
def slapd_sock_hanlder(ldap_reciever) -> SlapdSockHandler:
    return SlapdSockHandler(ldap_reciever)


@pytest.mark.parametrize("ldap_reciever", [True, False], indirect=["ldap_reciever"])
def test_ldap_reciever_startup(ldap_reciever: LDAPReciever):
    assert ldap_reciever


@pytest.mark.parametrize(
    "dn",
    [
        "cn=uidNumber,cn=temporary,cn=univention,dc=univention-organization,dc=intranet",
        "cn=4f8f67ac-3208-11ef-9700-ffb78fde9291,cn=groupName,cn=temporary,cn=univention,dc=univention-organization,dc=intranet",
    ],
)
def test_is_temporary_dn(ldap_reciever: LDAPReciever, dn):
    request = MagicMock()
    request.dn = dn
    assert ldap_reciever.filter_temporary_dn(request) is True


def test_is_not_temporary_dn(ldap_reciever: LDAPReciever):
    request = MagicMock()
    request.dn = "uid=0334afa8-32f7-11ef-9700-ffb78fde9291,cn=users,dc=univention-organization,dc=intranet"

    assert ldap_reciever.filter_temporary_dn(request) is False


@pytest.mark.asyncio
@pytest.mark.parametrize("ldap_reciever", [True, False], indirect=["ldap_reciever"])
async def test_handle_simple_udm_message(
    slapd_sock_hanlder: SlapdSockHandler, ldap_reciever: LDAPReciever, outgoing_queue: asyncio.Queue
):
    binary_request = b"RESULT\nmsgid: 281\nbinddn: cn=admin,dc=univention-organization,dc=intranet\npeername: IP=172.26.29.3:54846\nconnid: 1001\ncode: 0\ndn: cn=4f8f67ac-3208-11ef-9700-ffb78fde9291,cn=groups,dc=univention-organization,dc=intranet\ncontrol: 1.3.6.1.1.13.2 false ZIIDkQRYY249NGY4ZjY3YWMtMzIwOC0xMWVmLTk3MDAtZmZiNzhmZGU5MjkxLGNuPWdyb3VwcyxkYz11bml2ZW50aW9uLW9yZ2FuaXphdGlvbixkYz1pbnRyYW5ldDCCAzMwLAQCY24xJgQkNGY4ZjY3YWMtMzIwOC0xMWVmLTk3MDAtZmZiNzhmZGU5MjkxMBMECWdpZE51bWJlcjEGBAQ1MDA4MBUEDnNhbWJhR3JvdXBUeXBlMQMEATIwJAQTdW5pdmVudGlvbkdyb3VwVHlwZTENBAstMjE0NzQ4MzY0NjAiBAhzYW1iYVNJRDEWBBRTLTEtNS0yMS1VTlNFVC0xMTAxNzBWBAtvYmplY3RDbGFzczFHBBFzYW1iYUdyb3VwTWFwcGluZwQKcG9zaXhHcm91cAQDdG9wBA91bml2ZW50aW9uR3JvdXAEEHVuaXZlbnRpb25PYmplY3QwJgQUdW5pdmVudGlvbk9iamVjdFR5cGUxDgQMZ3JvdXBzL2dyb3VwMCUEFXN0cnVjdHVyYWxPYmplY3RDbGFzczEMBApwb3NpeEdyb3VwMDMECWVudHJ5VVVJRDEmBCQwZTMwNDgyMC1jNjU0LTEwM2UtOTg3Yi1iMzRlNjg0YjQ5ODEwQQQMY3JlYXRvcnNOYW1lMTEEL2NuPWFkbWluLGRjPXVuaXZlbnRpb24tb3JnYW5pemF0aW9uLGRjPWludHJhbmV0MCQED2NyZWF0ZVRpbWVzdGFtcDERBA8yMDI0MDYyNDA5MDExNFowNgQIZW50cnlDU04xKgQoMjAyNDA2MjQwOTAxMTQuODY1ODMzWiMwMDAwMDAjMDAwIzAwMDAwMDBCBA1tb2RpZmllcnNOYW1lMTEEL2NuPWFkbWluLGRjPXVuaXZlbnRpb24tb3JnYW5pemF0aW9uLGRjPWludHJhbmV0MCQED21vZGlmeVRpbWVzdGFtcDERBA8yMDI0MDYyNDA5MDExNFowZQQHZW50cnlETjFaBFhjbj00ZjhmNjdhYy0zMjA4LTExZWYtOTcwMC1mZmI3OGZkZTkyOTEsY249Z3JvdXBzLGRjPXVuaXZlbnRpb24tb3JnYW5pemF0aW9uLGRjPWludHJhbmV0MCMEEXN1YnNjaGVtYVN1YmVudHJ5MQ4EDGNuPVN1YnNjaGVtYTAaBA9oYXNTdWJvcmRpbmF0ZXMxBwQFRkFMU0U=\nchangetype: add\ncn: 4f8f67ac-3208-11ef-9700-ffb78fde9291\ngidNumber: 5008\nsambaGroupType: 2\nuniventionGroupType: -2147483646\nsambaSID: S-1-5-21-UNSET-11017\nobjectClass: sambaGroupMapping\nobjectClass: posixGroup\nobjectClass: top\nobjectClass: univentionGroup\nobjectClass: univentionObject\nuniventionObjectType: groups/group\nstructuralObjectClass: posixGroup\nentryUUID: 0e304820-c654-103e-987b-b34e684b4981\ncreatorsName: cn=admin,dc=univention-organization,dc=intranet\ncreateTimestamp: 20240624090114Z\nentryCSN: 20240624090114.865833Z#000000#000#000000\nmodifiersName: cn=admin,dc=univention-organization,dc=intranet\nmodifyTimestamp: 20240624090114Z\n\n"  # noqa E501

    reader = AsyncMock()
    reader.read = AsyncMock(return_value=binary_request)
    writer = MagicMock()
    ldap_reciever.legacy_backpressure_queue.put((123, 456, time.perf_counter()))

    await slapd_sock_hanlder.handle(reader, writer)

    pprint([event._asdict() for event in list(outgoing_queue._queue)])

    assert outgoing_queue.qsize() == 1
    result = await outgoing_queue.get()

    assert result.request_type == RequestType.add
    assert result.binddn == "cn=admin,dc=univention-organization,dc=intranet"
    assert result.old is None
    assert result.new == {
        "cn": [b"4f8f67ac-3208-11ef-9700-ffb78fde9291"],
        "gidNumber": [b"5008"],
        "sambaGroupType": [b"2"],
        "univentionGroupType": [b"-2147483646"],
        "sambaSID": [b"S-1-5-21-UNSET-11017"],
        "objectClass": [b"sambaGroupMapping", b"posixGroup", b"top", b"univentionGroup", b"univentionObject"],
        "univentionObjectType": [b"groups/group"],
        "structuralObjectClass": [b"posixGroup"],
        "entryUUID": [b"0e304820-c654-103e-987b-b34e684b4981"],
        "creatorsName": [b"cn=admin,dc=univention-organization,dc=intranet"],
        "createTimestamp": [b"20240624090114Z"],
        "entryCSN": [b"20240624090114.865833Z#000000#000#000000"],
        "modifiersName": [b"cn=admin,dc=univention-organization,dc=intranet"],
        "modifyTimestamp": [b"20240624090114Z"],
        "entryDN": [b"cn=4f8f67ac-3208-11ef-9700-ffb78fde9291,cn=groups,dc=univention-organization,dc=intranet"],
        "subschemaSubentry": [b"cn=Subschema"],
        "hasSubordinates": [b"FALSE"],
    }

    # RESULT requests don't expect a response from the socket backend.
    writer.write.assert_not_called()
    assert ldap_reciever.legacy_backpressure_queue.qsize() == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("ldap_reciever, queue_size", [(True, 0), (False, 1)], indirect=["ldap_reciever"])
async def test_handle_temporary_message(
    slapd_sock_hanlder: SlapdSockHandler, ldap_reciever: LDAPReciever, outgoing_queue: asyncio.Queue, queue_size
):
    binary_request = b"RESULT\nmsgid: 284\nbinddn: cn=admin,dc=univention-organization,dc=intranet\npeername: IP=172.26.29.3:54846\nconnid: 1001\ncode: 0\ndn: cn=5008,cn=gidNumber,cn=temporary,cn=univention,dc=univention-organization,dc=intranet\ncontrol: 1.3.6.1.1.13.1 false ZIICpwRWY249NTAwOCxjbj1naWROdW1iZXIsY249dGVtcG9yYXJ5LGNuPXVuaXZlbnRpb24sZGM9dW5pdmVudGlvbi1vcmdhbml6YXRpb24sZGM9aW50cmFuZXQwggJLMBoEC29iamVjdENsYXNzMQsEA3RvcAQEbG9jazAMBAJjbjEGBAQ1MDA4MBgECGxvY2tUaW1lMQwECjE3MTkyMTk5NzQwHwQVc3RydWN0dXJhbE9iamVjdENsYXNzMQYEBGxvY2swMwQJZW50cnlVVUlEMSYEJDBlMmM1MjEwLWM2NTQtMTAzZS05ODc4LWIzNGU2ODRiNDk4MTBBBAxjcmVhdG9yc05hbWUxMQQvY249YWRtaW4sZGM9dW5pdmVudGlvbi1vcmdhbml6YXRpb24sZGM9aW50cmFuZXQwJAQPY3JlYXRlVGltZXN0YW1wMREEDzIwMjQwNjI0MDkwMTE0WjA2BAhlbnRyeUNTTjEqBCgyMDI0MDYyNDA5MDExNC44Mzk4NzRaIzAwMDAwMCMwMDAjMDAwMDAwMEIEDW1vZGlmaWVyc05hbWUxMQQvY249YWRtaW4sZGM9dW5pdmVudGlvbi1vcmdhbml6YXRpb24sZGM9aW50cmFuZXQwJAQPbW9kaWZ5VGltZXN0YW1wMREEDzIwMjQwNjI0MDkwMTE0WjBjBAdlbnRyeUROMVgEVmNuPTUwMDgsY249Z2lkTnVtYmVyLGNuPXRlbXBvcmFyeSxjbj11bml2ZW50aW9uLGRjPXVuaXZlbnRpb24tb3JnYW5pemF0aW9uLGRjPWludHJhbmV0MCMEEXN1YnNjaGVtYVN1YmVudHJ5MQ4EDGNuPVN1YnNjaGVtYTAaBA9oYXNTdWJvcmRpbmF0ZXMxBwQFRkFMU0U=\nchangetype: delete\n\n"  # noqa E501

    reader = AsyncMock()
    reader.read = AsyncMock(return_value=binary_request)
    writer = MagicMock()
    ldap_reciever.legacy_backpressure_queue.put((123, 456, time.perf_counter()))

    await slapd_sock_hanlder.handle(reader, writer)

    pprint([event._asdict() for event in list(outgoing_queue._queue)])

    assert outgoing_queue.qsize() == queue_size


@pytest.mark.asyncio
@pytest.mark.parametrize("ldap_reciever, queue_size", [(True, 0), (False, 0)], indirect=["ldap_reciever"])
async def test_ignore_refint_overlay(
    slapd_sock_hanlder: SlapdSockHandler, ldap_reciever: LDAPReciever, outgoing_queue: asyncio.Queue, queue_size
):
    binary_request = b"MODIFY\nmsgid: 0\nbinddn: \npeername: \nconnid: 18446744073709551615\nsuffix: dc=univention-organization,dc=intranet\ndn: cn=Domain Users,cn=groups,dc=univention-organization,dc=intranet\ndelete: uniqueMember\nuniqueMember: uid=0ad4a8be-35f2-11ef-951b-37af858e1364,cn=users,dc=univention-organization,dc=intranet\n-\nreplace: modifiersName\nmodifiersName: cn=Referential Integrity Overlay\n-\n\n"  # noqa E501

    reader = AsyncMock()
    reader.read = AsyncMock(return_value=binary_request)
    writer = MagicMock()

    await slapd_sock_hanlder.handle(reader, writer)

    assert outgoing_queue.qsize() == 0
    assert len(ldap_reciever.legacy_backpressure_queue.queue) == 0
    writer.write.assert_called_once()
    assert writer.write.call_args_list[0].args[0] == CONTINUE_RESPONSE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_file, ldap_reciever, queue_size",
    [
        ("tests/unit/create_user_socket_requests.json", True, 2),
        ("tests/unit/create_user_socket_requests.json", False, 11),
        ("tests/unit/ldap_handler_test_data.json", True, 1),
        ("tests/unit/ldap_handler_test_data.json", False, 18),
        ("tests/unit/delete_requests_test_data.json", True, 3),
        ("tests/unit/delete_requests_test_data.json", False, 3),
        ("tests/unit/provisioning_e2e_test_data.json", True, 11),
        ("tests/unit/provisioning_e2e_test_data.json", False, 65),
        ("tests/unit/dev-env-requests.json", True, 1),
        ("tests/unit/dev-env-requests.json", False, 1),
    ],
    indirect=["ldap_reciever"],
)
async def test_replay_socket_requests(
    slapd_sock_hanlder: SlapdSockHandler,
    ldap_reciever: LDAPReciever,
    outgoing_queue: asyncio.Queue,
    request_file,
    queue_size,
):
    request_list: list = get_test_data(request_file)

    for request in request_list:
        reader = AsyncMock()
        writer = MagicMock()
        reader.read = AsyncMock(return_value=request["request_data"])

        await slapd_sock_hanlder.handle(reader, writer)

        if writer.write.called:
            handler_response = writer.write.call_args_list[-1].args[0]
            error_response = handler_response == TIMEOUT_RESPONSE.encode("utf-8")

            if error_response:
                pprint(handler_response)
                pprint(request)
                pprint(ldap_reciever.legacy_backpressure_queue.queue)
            assert not error_response

    event_list = list(outgoing_queue._queue)
    pprint([event._asdict() for event in event_list])

    assert len(event_list) == queue_size
    assert len(ldap_reciever.legacy_backpressure_queue.queue) == 0

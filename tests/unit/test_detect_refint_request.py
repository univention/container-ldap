# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

"""
MODIFY\n
msgid: 0\n
binddn: \n
peername: \n
connid: 18446744073709551615\n
suffix: dc=univention-organization,dc=intranet\n
dn: cn=Domain Users,cn=groups,dc=univention-organization,dc=intranet\n
delete: uniqueMember\n
uniqueMember: uid=0ad4a8be-35f2-11ef-951b-37af858e1364,cn=users,dc=univention-organization,dc=intranet\n
-\n
replace: modifiersName\n
modifiersName: cn=Referential Integrity Overlay\n
-\n
\n
"""

import pytest

import slapdsock.message
from tests.unit.test_ldap_reciever import get_test_data
from univention.ldif_producer.ldap_reciever import LDAPReciever

binary_requests = [
    b"MODIFY\nmsgid: 0\nbinddn: \npeername: \nconnid: 18446744073709551615\nsuffix: dc=univention-organization,dc=intranet\ndn: cn=Domain Users,cn=groups,dc=univention-organization,dc=intranet\ndelete: uniqueMember\nuniqueMember: uid=0ad4a8be-35f2-11ef-951b-37af858e1364,cn=users,dc=univention-organization,dc=intranet\n-\nreplace: modifiersName\nmodifiersName: cn=Referential Integrity Overlay\n-\n\n"  # noqa E501
    b"RESULT\nmsgid: 0\nbinddn: \npeername: \nconnid: 18446744073709551615\ncode: 0\ndn: cn=Domain Users,cn=groups,dc=univention-organization,dc=intranet\nchangetype: modify\ndelete: uniqueMember\nuniqueMember: uid=2e94b2ee-36b5-11ef-951b-37af858e1364,cn=users,dc=univention-organization,dc=intranet\n-\nreplace: modifiersName\nmodifiersName: cn=Referential Integrity Overlay\n-\n\n"  # noqa E501
    b"MODIFY\nmsgid: 0\nbinddn: \npeername: \nconnid: 18446744073709551615\nsuffix: dc=univention-organization,dc=intranet\ndn: cn=Domain Users,cn=groups,dc=univention-organization,dc=intranet\ndelete: uniqueMember\nuniqueMember: uid=2e94b2ee-36b5-11ef-951b-37af858e1364,cn=users,dc=univention-organization,dc=intranet\n-\nreplace: modifiersName\nmodifiersName: cn=Referential Integrity Overlay\n-\n\n"  # noqa E501
]


@pytest.mark.parametrize("binary_request", binary_requests)
def test_detect_modifiersName(binary_request):
    req_lines = binary_request.split(b"\n")
    assert LDAPReciever.is_refint_request(req_lines)


def test_empty_list():
    assert not LDAPReciever.is_refint_request([])


def test_detect_not_modifiersName():
    assert not LDAPReciever.is_refint_request([b"foo", b"bar", b"baz"])


@pytest.mark.parametrize("binary_request", binary_requests)
def test_create_request_class(binary_request):
    req_lines = binary_request.split(b"\n")
    request = slapdsock.message.MODIFYRequest(req_lines)
    assert request
    assert LDAPReciever.is_refint_request(request._req_lines)


def test_many_messages():
    request_list = get_test_data("tests/unit/create_user_socket_requests.json")
    request_list.extend(get_test_data("tests/unit/ldap_handler_test_data.json"))

    for request in request_list:
        request_lines = request["request_data"].split(b"\n")
        assert not LDAPReciever.is_refint_request(request_lines)

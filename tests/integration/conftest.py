# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

# pylint: disable=redefined-outer-name

import pytest
from ldap3 import ALL, Connection, ObjectDef, Server, Writer
from ldap3.utils.dn import safe_dn


@pytest.fixture(scope="session")
def connection(ldap_server, admin_dn, admin_password):
    """Connection to LDAP server."""
    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, admin_dn, admin_password, auto_bind=True)
    return conn


@pytest.fixture(scope="session")
def test_dn(base_dn):
    """Base container for objects from the test run."""
    ou_dn = safe_dn(["ou=tmp-testrunner", base_dn])
    return ou_dn


@pytest.fixture(scope="session")
def container(connection, test_dn):
    organizational_unit = ObjectDef(["organizationalUnit"], connection)
    writer = Writer(connection, organizational_unit)
    testrunner_container = writer.new(test_dn)
    writer.commit()
    if writer.failed:
        print(writer.errors)
    assert not writer.failed, "Creating the container in LDAP failed, manual cleanup required."

    yield testrunner_container

    testrunner_container.entry_refresh()
    testrunner_container.entry_delete()
    writer.commit()

    if writer.failed:
        print(writer.errors)
    assert not writer.failed, "Cleanup from LDAP failed, tests are leaking. Manual cleanup required."

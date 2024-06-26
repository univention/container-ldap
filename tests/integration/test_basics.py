# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2024 Univention GmbH

import pytest

from ldap3 import ObjectDef, Writer


@pytest.mark.timeout(1)
def test_ldap_server_can_be_searched(connection, admin_dn):
    connection.search(
        admin_dn,
        "(objectclass=person)",
        attributes=["sn", "objectclass"],
    )
    assert len(connection.entries) >= 1


@pytest.mark.timeout(1)
def test_create_entry_in_testrunner_container(connection, container):
    organizational_unit = ObjectDef(["organizationalUnit"], connection)
    writer = Writer(connection, organizational_unit)

    child = writer.new("ou=child," + container.entry_dn)
    assert writer.commit()

    child.entry_delete()
    assert writer.commit()

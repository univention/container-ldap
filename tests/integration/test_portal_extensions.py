# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

import pytest

from ldap3 import ObjectDef, Writer


@pytest.mark.timeout(1)
def test_ldap_server_can_be_reached(connection, admin_dn):
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


@pytest.mark.timeout(1)
def test_create_portal_entry(connection, container):
    portal_entry = ObjectDef(["univentionNewPortalEntry"], connection)
    writer = Writer(connection, portal_entry)

    entry = writer.new("cn=test-portal-entry," + container.entry_dn)
    assert writer.commit()

    entry.entry_delete()
    assert writer.commit()


@pytest.mark.timeout(1)
def test_create_portal_announcement(connection, container):
    portal_announcement = ObjectDef(
        ["univentionNewPortalAnnouncement"],
        connection,
    )
    writer = Writer(connection, portal_announcement)

    announcement = writer.new(
        "cn=test-portal-announcement," + container.entry_dn,
    )
    assert writer.commit()

    announcement.entry_delete()
    assert writer.commit()

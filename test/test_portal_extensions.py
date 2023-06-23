import pytest
from ldap3 import ObjectDef, Writer


def test_ldap_server_can_be_reached(connection, admin_dn):
    connection.search(
        admin_dn, "(objectclass=person)", attributes=["sn", "objectclass"])
    assert len(connection.entries) >= 1


def test_create_entry_in_testrunner_container(connection, container):
    organizationalUnit = ObjectDef(["organizationalUnit"], connection)
    writer = Writer(connection, organizationalUnit)

    child = writer.new("ou=child," + container.entry_dn)
    assert writer.commit()

    child.entry_delete()
    assert writer.commit()


def test_create_portal_entry(connection, container):
    portalEntry = ObjectDef(["univentionNewPortalEntry"], connection)
    writer = Writer(connection, portalEntry)

    entry = writer.new("cn=test-portal-entry," + container.entry_dn)
    assert writer.commit()

    entry.entry_delete()
    assert writer.commit()


@pytest.mark.xfail(
    reason="TODO: Add recent portal schema extensions with announcements")
def test_create_portal_announcement(connection, container):
    portalAnnouncement = ObjectDef(["univentionNewPortalAnnouncement"], connection)
    writer = Writer(connection, portalAnnouncement)

    announcement = writer.new("cn=test-portal-announcement," + container.entry_dn)
    assert writer.commit()

    announcement.entry_delete()
    assert writer.commit()

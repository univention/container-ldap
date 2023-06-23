import pytest


def test_ldap_server_can_be_reached(connection, admin_dn):
    connection.search(
        admin_dn, "(objectclass=person)", attributes=["sn", "objectclass"])
    assert len(connection.entries) >= 1


def test_create_testrunner_container_low_level(connection, test_dn):
    connection.add(test_dn, "organizationalUnit")
    connection.search(test_dn, "(objectClass=organizationalUnit)")
    assert len(connection.entries) == 1
    connection.delete(test_dn)
    connection.search(test_dn, "(objectClass=organizationalUnit)")
    assert len(connection.entries) == 0

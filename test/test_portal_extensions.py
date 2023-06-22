import pytest
from ldap3 import Server, Connection, ALL


@pytest.fixture(scope="session")
def connection(pytestconfig):
    """Connection to LDAP server."""
    server = Server(pytestconfig.getoption("--ldap-server"), get_info=ALL)
    admin_dn = pytestconfig.getoption("--ldap-admin-dn")
    admin_password = pytestconfig.getoption("--ldap-admin-password")
    conn = Connection(server, admin_dn, admin_password, auto_bind=True)
    return conn


def test_ldap_server_can_be_reached(connection, admin_dn):
    connection.search(
        admin_dn, "(objectclass=person)", attributes=["sn", "objectclass"])
    assert len(connection.entries) >= 1

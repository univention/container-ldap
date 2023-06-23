import pytest
from ldap3 import ALL, Connection, ObjectDef, Server, Writer
from ldap3.utils.dn import safe_dn


def pytest_addoption(parser):
    parser.addoption(
        "--ldap-server", action="store", default="localhost",
        help="LDAP server hostname to run tests against.")
    parser.addoption(
        "--ldap-admin-dn", action="store", default="cn=admin,dc=univention-organization,dc=intranet",
        help="DN of the admin account to use to bind to the LDAP server.")
    parser.addoption(
        "--ldap-admin-password", action="store", default="univention",
        help="Password to use to bind to the LDAP server.")
    parser.addoption(
        "--ldap-base-dn", action="store", default="dc=univention-organization,dc=intranet",
        help="Base DN of the LDAP directory.")


@pytest.fixture(scope="session")
def base_dn(pytestconfig):
    """Base DN of the LDAP server."""
    return pytestconfig.getoption("--ldap-base-dn")


@pytest.fixture(scope="session")
def admin_dn(pytestconfig):
    """Admin DN."""
    return pytestconfig.getoption("--ldap-admin-dn")


@pytest.fixture(scope="session")
def connection(pytestconfig):
    """Connection to LDAP server."""
    server = Server(pytestconfig.getoption("--ldap-server"), get_info=ALL)
    admin_dn = pytestconfig.getoption("--ldap-admin-dn")
    admin_password = pytestconfig.getoption("--ldap-admin-password")
    conn = Connection(server, admin_dn, admin_password, auto_bind=True)
    return conn


@pytest.fixture(scope="session")
def test_dn(base_dn):
    """Base container for objects from the test run."""
    ou_dn = safe_dn(["ou=tmp-testrunner", base_dn])
    return ou_dn


@pytest.fixture(scope="session")
def container(connection, test_dn):
    organizationalUnit = ObjectDef(["organizationalUnit"], connection)
    writer = Writer(connection, organizationalUnit)
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

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--ldap-server",
        action="store",
        default="localhost",
        help="LDAP server hostname to run tests against.",
    )
    parser.addoption(
        "--ldap-admin-dn",
        action="store",
        default="cn=admin,dc=univention-organization,dc=intranet",
        help="DN of the admin account to use to bind to the LDAP server.",
    )
    parser.addoption(
        "--ldap-admin-password",
        action="store",
        default="univention",
        help="Password to use to bind to the LDAP server.",
    )
    parser.addoption(
        "--ldap-base-dn",
        action="store",
        default="dc=univention-organization,dc=intranet",
        help="Base DN of the LDAP directory.",
    )


@pytest.fixture(scope="session")
def ldap_server(pytestconfig):
    """LDAP server name."""
    return pytestconfig.getoption("--ldap-server")


@pytest.fixture(scope="session")
def base_dn(pytestconfig):
    """Base DN of the LDAP server."""
    return pytestconfig.getoption("--ldap-base-dn")


@pytest.fixture(scope="session")
def admin_dn(pytestconfig):
    """Admin DN."""
    return pytestconfig.getoption("--ldap-admin-dn")


@pytest.fixture(scope="session")
def admin_password(pytestconfig):
    """Password for the Admin DN."""
    return pytestconfig.getoption("--ldap-admin-password")

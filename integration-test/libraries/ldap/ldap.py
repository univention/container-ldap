#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.

"""Robot framework library implementation for LDAP operations"""

import os
import ldap3

# If we are running as root then we assume
# that we are running in the docker-compose deployment
# on the same network as the LDAP server and it is accessible
# by the service name provided by docker-compose
# otherwise assume that ldap server is accessible locally
LDAP_SERVICE_NAME = 'openldap'
LOCAL_ADDRESS = '127.0.0.1'
LDAP_SERVER = LOCAL_ADDRESS if os.getuid() else LDAP_SERVICE_NAME
LDAP_URI = f'ldap://{LDAP_SERVER}:389'

LDAP_BASE_DN = 'dc=univention-organization,dc=intranet'

server = ldap3.Server(LDAP_URI)


def is_ldap_bind_successful(user, password):
    """Checks whether LDAP Bind works with the provided credentials"""
    try:
        conn = ldap3.Connection(
            server=server, user=user, password=password, auto_bind=False
        )
        return conn.bind()
    except ldap3.core.exceptions.LDAPPasswordIsMandatoryError:
        return False


def ldap_search(user, password, search_base, search_filter='(objectClass=*)'):
    """Checks whether LDAP Search works with the provided arguments"""
    try:
        with ldap3.Connection(
            server=server, user=user, password=password
        ) as conn:
            conn.search(search_base=search_base, search_filter=search_filter)
            return conn.entries
    except ldap3.core.exceptions.LDAPBindError:
        return ['LDAPBindError']


def ldap_add(user, password, ldap_dn, object_class=None, attributes=None):
    """Checks whether LDAP Add works with the provided arguments"""
    with ldap3.Connection(server=server, user=user, password=password) as conn:
        conn.add(dn=ldap_dn, object_class=object_class, attributes=attributes)
        return conn.result


def ldap_delete(user, password, ldap_dn):
    """Checks whether LDAP Delete works with the provided arguments"""
    with ldap3.Connection(server=server, user=user, password=password) as conn:
        conn.delete(dn=ldap_dn)
        return True


def ldap_modify(user, password, ldap_dn, updates):
    """Checks if LDAP Modiy works with the provided arguments"""
    changes = {k: [(ldap3.MODIFY_REPLACE, [v])] for k, v in updates.items()}
    with ldap3.Connection(server=server, user=user, password=password) as conn:
        conn.modify(dn=ldap_dn, changes=changes)
        return True


def ldap_search_without_bind(search_base, search_filter='(objectClass=*)'):
    """Checks whether LDAP Search works without authentication"""
    return ldap_operation_without_bind(
        lambda conn: conn.
        search(search_base=search_base, search_filter=search_filter)
    )


def ldap_add_without_bind(ldap_dn, object_class=None, attributes=None):
    """Checks whether LDAP Add works without authentication"""
    return ldap_operation_without_bind(
        lambda conn: conn.
        add(dn=ldap_dn, object_class=object_class, attributes=attributes)
    )


def ldap_modify_without_bind(ldap_dn, changes):
    """Checks whether LDAP Modify works without authentication"""
    return ldap_operation_without_bind(
        lambda conn: conn.modify(dn=ldap_dn, changes=changes)
    )


def ldap_operation_without_bind(operation):
    """Checks whether LDAP Operation works without authentication"""
    try:
        with ldap3.Connection(
            server=server,
            auto_bind='NONE',
            authentication='ANONYMOUS',
            raise_exceptions=True
        ) as conn:
            conn.open()
            operation(conn)
            return conn.result
    except ldap3.core.exceptions.LDAPStrongerAuthRequiredResult:
        return ['LDAPStrongerAuthRequiredResult']
    except ldap3.core.exceptions.LDAPChangeError:
        return ['LDAPChangeError']
    except ldap3.core.exceptions.LDAPInsufficientAccessRightsResult:
        return ['LDAPInsufficientAccessRightsResult']


def entry_to_dn(entry):
    """Returns the DN (str) of an ldap3.abstract.entry.Entry type of object"""
    return entry.entry_dn


def entry_to_ldif(entry):
    """Converts ldap3.abstract.entry.Entry type to LDIF (str) format"""
    return entry.entry_to_ldif()


def entry_to_json(entry):
    """Converts ldap3.abstract.entry.Entry type to JSON (str) format"""
    return entry.entry_to_json()

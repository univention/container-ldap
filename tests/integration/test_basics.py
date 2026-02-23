# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2025 Univention GmbH

import pytest
from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, ObjectDef, Writer


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


def clean_changes(connection):
    for entry in get_changes(connection):
        connection.delete(entry.entry_dn)


def get_changes(connection):
    connection.search("cn=changes", "(reqStart=*)", attributes=["*", "+"])
    return connection.entries


def accesslog_to_listener_new(change):
    new = {}
    for attr in change.reqMod.raw_values:
        key, value = attr.decode("UTF-8").split(":+ ", 1)
        new.setdefault(key, []).append(value.encode())
    return new


def accesslog_to_listener_old(change):
    old = {}
    for attr in change.reqOld.raw_values:
        key, value = attr.decode("UTF-8").split(": ", 1)
        old.setdefault(key, []).append(value.encode())
    return old


def accesslog_to_listener_modify(change):
    old = {}
    new = {}
    updated = []
    remove_from = {}
    for attr in change.reqOld.raw_values:
        key, value = attr.decode("UTF-8").split(": ", 1)
        old.setdefault(key, []).append(value.encode())
        new.setdefault(key, []).append(value.encode())
    for attr in change.reqMod.raw_values:
        attr = attr.decode("UTF-8")
        # new
        if ":+ " in attr:
            key, value = attr.split(":+ ", 1)
            new.setdefault(key, []).append(value.encode())
        # del
        elif attr.endswith(":-"):
            key = attr[:-2]
            del new[key]
        # del from
        elif ":- " in attr:
            key, value = attr.split(":- ", 1)
            remove_from.setdefault(key, []).append(value.encode())
        # modify
        elif ":= " in attr:
            key, value = attr.split(":= ", 1)
            if key not in updated:
                del new[key]
                updated.append(key)
            new.setdefault(key, []).append(value.encode())
    # remove elements from multi value
    for attr, remove_list in remove_from.items():
        new[attr] = [x for x in new[attr] if x not in remove_list]
    return new, old


def accesslog_to_listener(change):
    dn = change.reqDN.value
    old = None
    new = None
    command = None
    if change.reqType.value == "add":
        command = "a"
        new = accesslog_to_listener_new(change)
        new["entryDN"] = change.reqDN.raw_values
    elif change.reqType.value == "delete":
        command = "d"
        old = accesslog_to_listener_old(change)
        old["entryDN"] = change.reqDN.raw_values
    elif change.reqType.value == "modify":
        command = "m"
        new, old = accesslog_to_listener_modify(change)
        old["entryDN"] = change.reqDN.raw_values
        new["entryDN"] = change.reqDN.raw_values

    return dn, new, old, command


def get(connection, dn):
    connection.search(dn, "(objectclass=*)", attributes=["*", "+"])
    return connection.entries[0]


def ldap_diff(attrs, expected):
    del expected["hasSubordinates"]  # we dont have this in accesslog
    del expected["subschemaSubentry"]  # we dont have this in accesslog
    if set(attrs.keys()) != set(expected.keys()):
        return True
    changed_keys = {k for k in expected.keys() & attrs.keys() if set(expected[k]) != set(attrs[k])}
    if changed_keys:
        return True
    return False


def test_changes_add(connection, container):
    clean_changes(connection)
    person = ObjectDef(["person", "univentionObject"], connection)
    writer = Writer(connection, person)
    child = writer.new("cn=person," + container.entry_dn)
    child.sn = "surename"
    child.telephoneNumber = ["1", "2"]
    child.univentionObjectType = "my/object"
    assert writer.commit()
    child_obj = get(connection, child.entry_dn)
    change = get_changes(connection)[0]
    dn, new, old, command = accesslog_to_listener(change)
    assert dn == child.entry_dn
    assert command == "a"
    assert old is None
    assert not ldap_diff(new, child_obj.entry_raw_attributes)
    child.entry_delete()
    assert writer.commit()


def test_changes_delete(connection, some_ldap_object):
    clean_changes(connection)
    assert connection.delete(some_ldap_object.entry_dn)
    change = get_changes(connection)[0]
    dn, new, old, command = accesslog_to_listener(change)
    assert dn == some_ldap_object.entry_dn
    assert command == "d"
    assert new is None
    assert not ldap_diff(old, some_ldap_object.entry_raw_attributes)


def test_changes_modify(connection, some_ldap_object):
    clean_changes(connection)
    assert "description" not in some_ldap_object.entry_attributes
    assert "mailAlternativeAddress" not in some_ldap_object.entry_attributes
    assert some_ldap_object.gecos
    assert some_ldap_object.mail
    assert some_ldap_object.gidNumber
    assert some_ldap_object.telephoneNumber
    assert some_ldap_object.mobile
    assert some_ldap_object.pager
    modification = {
        # add single value attr
        "description": [(MODIFY_ADD, ["fdsfsf"])],
        # add multi value attr
        "mailAlternativeAddress": [(MODIFY_ADD, ["a@b", "c@d"])],
        # delete single value attr
        "gecos": [(MODIFY_DELETE, [])],
        "mail": [(MODIFY_DELETE, [])],
        # modify single value attr
        "gidNumber": [(MODIFY_REPLACE, ["99"])],
        # modify multi value attr
        "telephoneNumber": [(MODIFY_REPLACE, ["1", "3"])],
        # modify multi value remove some value
        "mobile": [(MODIFY_DELETE, ["1", "3"])],
        # modify multi value add some value
        "pager": [(MODIFY_ADD, ["4243", "43242"])],
    }
    connection.modify(some_ldap_object.entry_dn, modification)
    expected_new = get(connection, some_ldap_object.entry_dn)
    change = get_changes(connection)[0]
    dn, new, old, command = accesslog_to_listener(change)
    assert dn == some_ldap_object.entry_dn
    assert command == "m"
    assert not ldap_diff(old, some_ldap_object.entry_raw_attributes)
    assert not ldap_diff(new, expected_new.entry_raw_attributes)


def test_changes_rename(connection, some_ldap_object):
    clean_changes(connection)
    # breakpoint()

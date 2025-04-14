# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import os


def test_parse_attributes(sync_ldap_indexes, schema_file):
    expected_attributes = {"univentionObjectIdentifier": {"equality": "uuidMatch"}}
    parsed_attributes = sync_ldap_indexes.parse_attributes(schema_file)

    assert expected_attributes == parsed_attributes


def test_get_attributes_from_schemas(sync_ldap_indexes):
    file_path = f"{os.path.abspath(os.path.dirname(__file__))}/ldap-testfiles"
    expected_attributes = {
        "univentionObjectIdentifier": {
            "equality": "uuidMatch",
            "schema_file": f"{file_path}/test-ldap-schema.schema",
        },
        "univentionObjectIdentifier2": {
            "equality": "uuidMatch",
            "schema_file": f"{file_path}/test-ldap-schema-2.schema",
        },
    }
    parsed_attributes = sync_ldap_indexes.get_attributes_from_schemas([file_path])

    assert expected_attributes == parsed_attributes


def test_get_current_indexes(sync_ldap_indexes):
    expected_indexes = {
        "eq": ["univentionObjectIdentifier", "newAttrToIndex"],
        "pres": ["univentionObjectIdentifier", "newAttrToIndex"],
        "approx": ["univentionObjectIdentifier", "newAttrToIndex"],
        "sub": ["univentionObjectIdentifier", "newAttrToIndex"],
    }
    current_indexes = sync_ldap_indexes.get_current_indexes()

    assert expected_indexes == current_indexes


def test_get_changed_attributes(sync_ldap_indexes, schema_file):
    expected_attributes = ["univentionObjectIdentifier", "newAttrToIndex"]

    attributes = sync_ldap_indexes.parse_attributes(schema_file)
    indexes = sync_ldap_indexes.get_current_indexes()
    state = sync_ldap_indexes.get_state(indexes, attributes)

    # statefile_indexes = ["univentionObjectIdentifier"]
    file_path = os.path.abspath(os.path.dirname(__file__))
    statefile_state = sync_ldap_indexes.get_state_from_file(f"{file_path}/ldap-testfiles/test-ldap-statefile.json")

    changed_attributes = sync_ldap_indexes.get_changed_attributes(statefile_state, state)

    assert expected_attributes == changed_attributes

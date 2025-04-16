# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH
import logging
import os
from json import JSONDecodeError
from pathlib import Path

import pytest


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

    file_path = os.path.abspath(os.path.dirname(__file__))
    statefile_state = sync_ldap_indexes.read_state_file(Path(f"{file_path}/ldap-testfiles/test-ldap-statefile.json"))

    changed_attributes = sync_ldap_indexes.get_changed_attributes(statefile_state, state)

    assert expected_attributes == changed_attributes


def test_broken_state_file(sync_ldap_indexes):
    file_path = os.path.abspath(os.path.dirname(__file__))
    with pytest.raises(JSONDecodeError):
        sync_ldap_indexes.read_state_file(Path(f"{file_path}/ldap-testfiles/test-ldap-statefile-broken.json"))


def test_main_function_broken_state_file(sync_ldap_indexes, caplog):
    file_path = os.path.abspath(os.path.dirname(__file__))
    schema_dirs = [Path(f"{file_path}/ldap-testfiles/")]
    state_file_path = Path(f"{file_path}/ldap-testfiles/test-ldap-statefile-broken.json")
    state_file_template_path = Path(f"{file_path}/ldap-testfiles/test-ldap-statefile.json")
    mdb_file_path = Path(f"{file_path}/ldap-testfiles/data.mdb")

    sync_ldap_indexes.main(schema_dirs, state_file_path, state_file_template_path, mdb_file_path)

    assert len(caplog.records) == 1

    assert caplog.records[0].levelno == logging.ERROR
    assert "Error reading state file" in caplog.records[0].message


def test_main_function(sync_ldap_indexes, caplog):
    file_path = os.path.abspath(os.path.dirname(__file__))
    schema_dirs = [Path(f"{file_path}/ldap-testfiles/")]
    state_file_path = Path(f"{file_path}/ldap-testfiles/test-ldap-statefile-tmp.json")
    state_file_template_path = Path(f"{file_path}/ldap-testfiles/test-ldap-statefile.json")
    mdb_file_path = Path(f"{file_path}/ldap-testfiles/data.mdb")

    sync_ldap_indexes.main(schema_dirs, state_file_path, state_file_template_path, mdb_file_path)

    # assert len(caplog.records) == 1
    #
    # assert caplog.records[0].levelno == logging.ERROR
    # assert "Error reading state file" in caplog.records[0].message

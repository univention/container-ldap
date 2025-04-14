#!/usr/bin/python
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2024 Univention GmbH

import glob
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pprint import pprint

from deepdiff import DeepDiff

from univention.config_registry import ucr


def parse_attributes(file_content: str) -> dict:
    """
    Parses the given string for the LDAP attributetype settings and returns
    the name and equality parameters as dictionary.

    attributetype example:
    ----------------------
    attributetype ( 1.3.6.1.4.1.10176.1003.3 NAME 'univentionObjectIdentifier'
        DESC 'ASCII string representation of a permanent IAM object identifier,
              like entryUUID or Active Directroy objectGUID'
        EQUALITY uuidMatch
        ORDERING UUIDOrderingMatch
        SYNTAX 1.3.6.1.1.16.1 SINGLE-VALUE )
    """
    attributes = {}

    pattern = r"attributetype\s+\((.+)((?:\n.+)+)\)"
    matches = re.findall(pattern, file_content, re.MULTILINE)

    for mg in matches:
        attribute_name = None
        equality = None

        for m in mg:
            pattern = r".+NAME\s+\'(.*)\'"
            match = re.search(pattern, m)
            if match:
                attribute_name = match[1]

            pattern = r".+EQUALITY\s+([\w]+)"
            match = re.search(pattern, m)
            if match:
                equality = match[1]

        if attribute_name and equality:
            attributes[attribute_name] = {
                "equality": equality,
            }

    return attributes


def get_current_indexes() -> dict:
    """
    Returns all configured indexes from UCR.
    """
    index_types = ["eq", "pres", "approx", "sub"]
    current_indexes = {}

    for index_type in index_types:
        indexes = ucr.get(f"ldap/index/{index_type}")
        current_indexes[index_type] = indexes.split(",")

    return current_indexes


def get_attributes_from_schemas(schema_dirs: list) -> dict:
    """
    Returns attributes with equality from all attributetype definitionsschema files.

    attributetype example:
    ----------------------
    attributetype ( 1.3.6.1.4.1.10176.1003.3 NAME 'univentionObjectIdentifier'
        DESC 'ASCII string representation of a permanent IAM object identifier,
              like entryUUID or Active Directroy objectGUID'
        EQUALITY uuidMatch
        ORDERING UUIDOrderingMatch
        SYNTAX 1.3.6.1.1.16.1 SINGLE-VALUE )
    """
    all_attributes = {}

    for schema_dir in schema_dirs:
        for schema_file in glob.glob(f"{schema_dir}/*.schema"):
            with open(os.path.join(schema_dir, schema_file)) as f:
                file_content = f.read()

                attributes = parse_attributes(file_content=file_content)
                for attr_name, attr_value in attributes.items():
                    attr_value["schema_file"] = schema_file

                all_attributes |= attributes

    return all_attributes


def get_state(current_indexes: dict, attributes: dict) -> dict:
    """
    Returns state from the current config.
    """
    state = {"attributes": {}}

    for index_type, index_attributes in current_indexes.items():
        for index_attribute in index_attributes:
            if not state["attributes"].get(index_attribute):
                state["attributes"][index_attribute] = {"indexes": []}
            state["attributes"][index_attribute]["indexes"].append(
                {
                    "type": index_type,
                    "last_reindex_date": datetime.now().strftime("%Y-%m-%d"),
                }
            )

    for attr_name, attr_val in attributes.items():
        if state.get("attributes").get(attr_name) and attr_val:
            state["attributes"][attr_name]["equality"] = attr_val.get("equality")
            state["attributes"][attr_name]["schema_file"] = attr_val.get("schema_file")

    return state


def get_state_from_file(statefile_path: str) -> dict:
    """
    Returnsstate from the statefile.
    """
    f = open(os.path.join(statefile_path))
    file_content = f.read()

    state = json.loads(file_content)

    return state


def get_changed_attributes(state_file: dict, current_state: dict) -> list:
    """
    Returns the name of all changed attributes.

    Compares the statefile with the current state.
    """
    differences = DeepDiff(
        t1=state_file["attributes"],
        t2=current_state["attributes"],
        exclude_regex_paths=[r"last_reindex_date", r"schema_file"],
        view="text",
        verbose_level=2,
    )

    pprint(differences)
    print()

    return differences.affected_root_keys


def get_ldap_base_dn():
    return os.environ.get("LDAP_BASEDN")


def main():
    schema_dirs = ["/usr/share/univention-ldap/schema", "/etc/ldap/schema"]
    statefile_path = "/var/lib/univention-ldap/ldap-index-statefile.json"
    orig_statefile_path = "/opt/univention/ldap-tools/ldap-index-statefile.json"

    # Check and create statefile
    if not os.path.isfile(statefile_path):
        shutil.copyfile(orig_statefile_path, statefile_path)

    # Get states
    current_state = get_state(
        current_indexes=get_current_indexes(),
        attributes=get_attributes_from_schemas(schema_dirs),
    )
    state_file = get_state_from_file(statefile_path)

    # Create diff
    # current_state["attributes"]["univentionObjectIdentifier"] = {"indexes": [{"type": "pres"}, {"type": "eq"}]}
    # current_state["attributes"]["univentionObjectFlag"]["equality"] = "caseIgnoreMatch"
    # current_state["attributes"]["univentionServerRole"]["indexes"].append({"type": "pres"})
    # current_state["attributes"]["cn"]["equality"] = "caseIgnoreMatch"
    # current_state["attributes"].pop("sambaSID")

    changed_attributes = get_changed_attributes(state_file=state_file, current_state=current_state)

    print("##### Commands:")
    for attribute_name in changed_attributes:
        command = f'slapindex -b "{get_ldap_base_dn()}" {attribute_name}'
        print(command)
        ans = subprocess.run(command, shell=True, executable="/bin/bash")
        if ans.returncode == 0:
            print(f"Command {command} executed successful: {ans.stdout}")
            # TODO Rewrite statefile
        else:
            print(f"SLAPINDEX ERROR: {command}: {ans.stderr}")


if __name__ == "__main__":
    main()

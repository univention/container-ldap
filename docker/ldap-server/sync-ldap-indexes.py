#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2024 Univention GmbH

import glob
import json
import os
import re
from pprint import pprint

from deepdiff import DeepDiff

from univention.config_registry import ucr


def get_current_indexes():
    index_types = ["eq", "pres", "approx", "sub"]
    current_indexes = {}

    for index_type in index_types:
        indexes = ucr.get(f"ldap/index/{index_type}")
        current_indexes[index_type] = indexes.split(",")

    return current_indexes


def get_attributes_from_schemas():
    schema_dirs = ["/usr/share/univention-ldap/schema", "/etc/ldap/schema"]
    attributes = {}

    for schema_dir in schema_dirs:
        for schema_file in glob.glob(f"{schema_dir}/*.schema"):
            with open(os.path.join(schema_dir, schema_file)) as f:
                file_content = f.read()

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
                            "schema_file": schema_file,
                        }

    return attributes


def get_state(current_indexes, attributes):
    state = {"attributes": {}}

    for index_type, index_attributes in current_indexes.items():
        for index_attribute in index_attributes:
            if not state["attributes"].get(index_attribute):
                state["attributes"][index_attribute] = {"indexes": []}
            state["attributes"][index_attribute]["indexes"].append({"type": index_type, "last_reindex_date": None})

    for attr_name, attr_val in attributes.items():
        if state.get("attributes").get(attr_name) and attr_val:
            state["attributes"][attr_name]["equality"] = attr_val.get("equality")
            state["attributes"][attr_name]["schema_file"] = attr_val.get("schema_file")

    return state


def get_state_from_file():
    statefile_dir = "/opt/univention/ldap-tools"
    statefile_name = "ldap-index-statefile.json"

    f = open(os.path.join(statefile_dir, statefile_name))
    file_content = f.read()

    state = json.loads(file_content)

    return state


# Get states
current_state = get_state(current_indexes=get_current_indexes(), attributes=get_attributes_from_schemas())
state_file = get_state_from_file()

# Create diff
current_state["attributes"]["univentionObjectIdentifier"] = {"indexes": [{"type": "pres"}, {"type": "eq"}]}
current_state["attributes"]["univentionObjectFlag"]["equality"] = "caseIgnoreMatch"
current_state["attributes"]["univentionServerRole"]["indexes"].append({"type": "pres"})

differences = DeepDiff(t1=state_file, t2=current_state, exclude_regex_paths=r"last_reindex_date")
pprint(differences)

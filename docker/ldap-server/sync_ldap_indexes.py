#!/usr/bin/python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2024 Univention GmbH

import glob
import json
import logging
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from pprint import pformat

from univention.config_registry import ucr


class NoIndexException(Exception):
    pass


class SlapindexException(Exception):
    pass

def get_logger():
    LOG_FORMAT = "%(asctime)s %(levelname)-5s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"
    LOG_LEVEL = os.environ.get("PYTHON_LOG_LEVEL") or "INFO"
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logger = logging.getLogger(__name__)
    return logger

logger = get_logger()

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
        current_indexes[index_type] = set(indexes.split(","))

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

    # Populate state with index information.
    for index_type, index_attributes in current_indexes.items():
        for index_attribute in index_attributes:
            if not state["attributes"].get(index_attribute):
                state["attributes"][index_attribute] = {"indexes": []}
            state["attributes"][index_attribute]["indexes"].append(
                {
                    "type": index_type,
                    "last_index_date": datetime.now().isoformat(),
                }
            )

    # Populate state with attribute information.
    for attr_name, attr_val in attributes.items():
        if state.get("attributes").get(attr_name) and attr_val:
            state["attributes"][attr_name]["equality"] = attr_val.get("equality")
            state["attributes"][attr_name]["schema_file"] = attr_val.get("schema_file")

    logger.debug(f"current state:\n{pformat(state)}")
    return state


def read_state_file(state_file_path: Path) -> dict:
    """
    Returns state from the state file.
    """
    with state_file_path.open("r") as f:
        file_content = f.read()

    state = json.loads(file_content)
    logger.debug(f"state from state file:\n{pformat(state)}")
    return state


def write_state_file(state_file_path: Path, state: dict):
    state_json = json.dumps(dict(sorted(state.items())), indent=4)
    with state_file_path.open("w") as f:
        f.write(state_json)


def attribute_needs_reindexing(new: dict, old: dict) -> bool:
    if not new or not old:
        return True
    if new.get("equality") != old.get("equality"):
        return True
    new_indexes = {i["type"] for i in new.get("indexes", [])}
    old_indexes = {i["type"] for i in old.get("indexes", [])}
    return new_indexes != old_indexes


def get_changed_attributes(new_state: dict, old_state: dict) -> list:
    differences = []
    new_attributes = new_state["attributes"]
    old_attributes = old_state["attributes"]

    for attribute in set(new_attributes) | set(old_attributes):
        if attribute_needs_reindexing(
            new_attributes.get(attribute, {}),
            old_attributes.get(attribute, {}),
        ):
            differences.append(attribute)
    return differences


def get_ldap_base_dn():
    return os.environ.get("LDAP_BASEDN")


def execute_slapindex(attribute_name: str):
    command = f'slapindex -b "{get_ldap_base_dn()}" {attribute_name}'
    ans = subprocess.run(command, shell=True, executable="/bin/bash", capture_output=True, text=True)
    if ans.returncode == 0:
        logger.info(f"Executed successful: {command} [{ans.stdout or '-'}]")

    else:
        if ans.stderr.find(f"mdb_tool_entry_reindex: no index configured for {attribute_name}") > -1:
            raise NoIndexException(f"Index for {attribute_name} is not configured.")
        else:
            raise SlapindexException(f"SLAPINDEX ERROR: {command}: {ans.stderr}")


def main(schema_dirs: list[str], state_file_path: Path, state_file_template_path: Path, mdb_file_path: Path):
    # Check ldap installation state.
    virgin_persistent_volume = not os.path.isfile(mdb_file_path) and not os.path.isfile(state_file_path)
    missing_state_file = not virgin_persistent_volume and not os.path.isfile(state_file_path)
    logger.debug(f"virgin_persistent_volume: {virgin_persistent_volume}")
    logger.debug(f"missing_state_file: {missing_state_file}")

    # Check and create state file
    if missing_state_file:
        shutil.copyfile(state_file_template_path, state_file_path)
        logger.info("Missing state file! New state file from template created.")

    # Get current state from ucr.
    current_state = get_state(
        current_indexes=get_current_indexes(),
        attributes=get_attributes_from_schemas(schema_dirs),
    )

    # On a clean installation, the state file is written with the current state.
    if virgin_persistent_volume:
        write_state_file(state_file_path, current_state)
        logger.info("Virgin persistent volume! New state file with current state created.")
        return

    # Read state file
    try:
        state_file = read_state_file(state_file_path)
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Error reading state file: {e}.")
        return

    # Check changed attributes.
    changed_attributes = get_changed_attributes(new_state=state_file, old_state=current_state)
    if not changed_attributes:
        logger.info("No changed attributes, nothing to do!")
        return

    # Execute slapindex for each changed attribute.
    for attribute_name in changed_attributes:
        logger.info(f"Processing attribute {attribute_name}.")
        try:
            execute_slapindex(attribute_name=attribute_name)

        except SlapindexException as e:
            logger.error(e)

        except NoIndexException as e:
            # If no index exists for an attribute,
            # the index is deleted from state.
            logger.info(f"{e} Index is deleted from state file.")
            state_file["attributes"].pop(attribute_name)

        else:
            # Update state
            state_file["attributes"][attribute_name] = current_state["attributes"][attribute_name]

    # Write current state to state file.
    logger.debug(f"new state:\n{pformat(state_file)}")
    write_state_file(state_file_path, state_file)


if __name__ == "__main__":
    main(
        schema_dirs=["/usr/share/univention-ldap/schema", "/etc/ldap/schema"],
        state_file_path=Path("/var/lib/univention-ldap/ldap-index-statefile.json"),
        state_file_template_path=Path("/opt/univention/ldap-tools/ldap-index-statefile.json"),
        mdb_file_path=Path("/var/lib/univention-ldap/ldap/data.mdb"),
    )

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging
import os
from pathlib import Path
from pprint import pformat
from typing import NamedTuple

import ldap
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config(NamedTuple):
    ldap_host: int | str
    ldap_port: int
    ldap_base_dn: str
    ldap_admin_user: str
    ldap_admin_password: str
    log_level: str


def get_config() -> Config:
    global logger

    file_path = os.path.dirname(__file__)
    env_file = Path(f"{file_path}/../.env.ldap-server")
    if env_file.is_file():
        load_dotenv(env_file)
    else:
        logger.warning("Environment file %s not found!", env_file)

    ldap_host = os.environ.get("LDAP_HOST")
    if not ldap_host:
        raise ValueError("Missing environment variable: LDAP_HOST")
    ldap_port = os.environ.get("LDAP_PORT")
    if not ldap_port:
        raise ValueError("Missing environment variable: LDAP_PORT")
    ldap_admin_user = os.environ.get("LDAP_ADMIN_USER")
    if not ldap_admin_user:
        raise ValueError("Missing environment variable: LDAP_ADMIN_USER")
    ldap_admin_password = os.environ.get("LDAP_ADMIN_PASSWORD")
    if not ldap_admin_password:
        raise ValueError("Missing environment variable: LDAP_ADMIN_PASSWORD")
    ldap_base_dn = os.environ.get("LDAP_BASE_DN")
    if not ldap_base_dn:
        raise ValueError("Missing environment variable: LDAP_BASE_DN")
    log_level = os.environ.get("PYTHON_LOG_LEVEL")
    if not log_level:
        raise ValueError("Missing environment variable: PYTHON_LOG_LEVEL")

    return Config(
        log_level=log_level,
        ldap_base_dn=ldap_base_dn,
        ldap_host=ldap_host,
        ldap_port=ldap_port,
        ldap_admin_user=ldap_admin_user,
        ldap_admin_password=ldap_admin_password,
    )


def setup_logging(level: str | int):
    log_format = "%(asctime)s %(levelname)-5s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"
    logging.basicConfig(format=log_format, level=level)
    global logger
    logger = logging.getLogger(__name__)


def ldap_connect(ldap_host: str, ldap_port: int, ldap_admin_user: str, ldap_admin_password: str, ldap_base_dn: str):
    global logger

    logger.debug("Try connect to %s (%s) with %s", f"ldap://{ldap_host}:{ldap_port}", ldap_base_dn, ldap_admin_user)

    try:
        ldap_connection = ldap.initialize(f"ldap://{ldap_host}:{ldap_port}")
    except ldap.SERVER_DOWN:
        logger.error("LDAP server down")
        exit(1)

    try:
        ldap_connection.simple_bind_s(f"cn={ldap_admin_user},{ldap_base_dn}", ldap_admin_password)
    except ldap.INVALID_CREDENTIALS:
        logger.error("Invalid LDAP credentials")
        exit(1)

    logger.debug("Connected to %s (%s) with %s", f"ldap://{ldap_host}:{ldap_port}", ldap_base_dn, ldap_admin_user)

    return ldap_connection


def update_univention_object_identifier(ldap_connection: ldap.ldapobject, ldap_base_dn: str):
    global logger

    result = ldap_connection.search_s(
        f"{ldap_base_dn}",
        ldap.SCOPE_SUBTREE,
        "(&(objectClass=univentionObject)(!(univentionObjectIdentifier=*)))",
        ["univentionObjectIdentifier", "entryUUID"],
    )

    cnt = 0
    for entry in result:
        logger.debug("Processing %s", entry[0])
        logger.debug("Values:\n%s", pformat(entry[1], indent=4))

        if not entry[1].get("univentionObjectIdentifier") and entry[1].get("entryUUID"):
            try:
                ldap_connection.modify_s(
                    entry[0],
                    [
                        (
                            ldap.MOD_REPLACE,
                            "univentionObjectIdentifier",
                            entry[1].get("entryUUID"),
                        )
                    ],
                )
            except Exception as e:
                logger.error(e)

            cnt += 1

    logger.info("Updated %s records.", cnt)


def main(config: Config):
    setup_logging(config.log_level)
    global logger
    logger.info("Updating univentionObjectIdentifier with entryUUID values.")
    logger.debug("Loaded config:\n%s", pformat(dict(config._asdict()), indent=4))

    ldap_connection = ldap_connect(
        ldap_host=config.ldap_host,
        ldap_port=config.ldap_port,
        ldap_admin_user=config.ldap_admin_user,
        ldap_admin_password=config.ldap_admin_password,
        ldap_base_dn=config.ldap_base_dn,
    )

    update_univention_object_identifier(ldap_connection=ldap_connection, ldap_base_dn=config.ldap_base_dn)


# ###########################################################################
# # Main
# ###########################################################################

if __name__ == "__main__":
    main(get_config())

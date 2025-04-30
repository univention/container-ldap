# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging
import os
import sys
from pathlib import Path
from pprint import pformat
from random import randrange
from typing import NamedTuple

import ldap
from dotenv import load_dotenv
from faker import Faker
from faker.providers import internet

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


def generate_fake_user_data(num_of_users: int):
    fake = Faker()
    fake.add_provider(internet)

    user_data = []
    for _ in range(num_of_users):
        username = fake.user_name()
        fullname = fake.name()
        lastname = fake.last_name()
        # email = fake.free_email()
        # Extending with a random number because of uniqueness
        uid = f"{username}{randrange(10000, 99999)}"

        ldap_user = [
            ("objectClass", [b"person", b"top", b"univentionObject", b"shadowAccount"]),
            ("uid", uid.encode()),
            ("cn", fullname.encode()),
            ("sn", lastname.encode()),
            ("userPassword", b"univention"),
            ("univentionObjectType", b"users/user"),
        ]
        user_data.append(ldap_user)

    return user_data


def create_user(user: dict, ldap_conn: ldap.ldapobject, ldap_base_dn: str):
    uid = [item for item in user if item[0] == "uid"][0][1].decode()
    logger.debug("Userdata:\n%s", pformat(user, indent=4))
    logger.debug("uid: %s", uid)

    dn = f"uid={uid},cn=users,{ldap_base_dn}"
    ldap_conn.add_s(dn, user)


def get_no_users():
    global logger
    usage = """---\n
        python ldap-create-fake-users.py NUMBER_OF_USERS

    """
    if len(sys.argv) < 2:
        logger.error("No number of users given!")
        print(usage)
        exit(1)

    try:
        no_users = int(sys.argv[1])
    except ValueError:
        logger.error("Number of users must be numeric!")
        print(usage)
        exit(1)

    return no_users


def main(config: NamedTuple):
    global logger
    setup_logging(config.log_level)

    no_users = get_no_users()

    logger.info("Startet fake user creation.")
    logger.debug("Number of users to create: %s", no_users)
    logger.debug("Loaded config:\n%s", pformat(dict(config._asdict()), indent=4))

    ldap_connection = ldap_connect(
        ldap_host=config.ldap_host,
        ldap_port=config.ldap_port,
        ldap_admin_user=config.ldap_admin_user,
        ldap_admin_password=config.ldap_admin_password,
        ldap_base_dn=config.ldap_base_dn,
    )

    users = generate_fake_user_data(num_of_users=no_users)

    cnt = 0
    for user in users:
        create_user(user, ldap_connection, ldap_base_dn=config.ldap_base_dn)
        cnt += 1
    logger.info("%i fake users created.", cnt)


# ##########################################################

main(get_config())

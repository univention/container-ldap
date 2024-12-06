#!/usr/bin/python
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import argparse
import logging
import sys

from kubernetes import client, config

logger = logging.getLogger(__name__)


CONFIGMAP_NAME = "nubus-deployment-status"
DATABASE_INITIALIZED_KEY = "ldap_database_initialized"


def database_needs_initialization(v1: client.CoreV1Api, namespace: str):
    """
    Check if the ConfigMap exists and has the key ldap_database_initialized set to true.

    Returns:
        0: Database needs initialization: ldap_database_initialized is set to false.
        1: Database already initialized: ldap_database_initialized is already true in the ConfigMap.
        2: LDAP server should terminate: Unexpected error accessing or parsing the ConfigMap.
    """

    try:
        configmap = v1.read_namespaced_config_map(name=CONFIGMAP_NAME, namespace=namespace)

        if DATABASE_INITIALIZED_KEY not in configmap.data:
            logger.error("ConfigMap does not contain the key `%s`." % DATABASE_INITIALIZED_KEY)
            raise ValueError("Invalid ConfigMap structure")

        if configmap.data[DATABASE_INITIALIZED_KEY].lower() == "true":
            logger.info("Database already initialized.")
            sys.exit(1)

    except Exception as error:
        logger.error("Unexpected error evaluating the database initialization status.")
        logger.error(error)
        sys.exit(2)

    logger.info("Database needs initialization.")
    sys.exit(0)


def database_initialized(v1: client.CoreV1Api, namespace: str):
    try:
        configmap = v1.read_namespaced_config_map(name=CONFIGMAP_NAME, namespace=namespace)

        if DATABASE_INITIALIZED_KEY not in configmap.data:
            logger.error("ConfigMap does not contain the key `%s`." % DATABASE_INITIALIZED_KEY)
            raise ValueError("Invalid ConfigMap structure")

        configmap.data[DATABASE_INITIALIZED_KEY] = "true"

        v1.replace_namespaced_config_map(name=CONFIGMAP_NAME, namespace=namespace, body=configmap)

    except Exception as error:
        logger.error("Unexpected error updating the database initialization status.")
        logger.error(error)
        sys.exit(2)
    logger.info("Database initialization status set to true in the %s ConfigMap" % CONFIGMAP_NAME)


def main():
    parser = argparse.ArgumentParser(
        description="Script to check LDAP database initialization status in Nubus for Kubernetes"
    )
    parser.add_argument("--log-level", default="info", help="Set the log level, default is INFO")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command_needs_initialization = subparsers.add_parser(
        "database-needs-initialization",
        help="Check the LDAP database initialization status, returns 0 if initialization is required.",
    )
    command_needs_initialization.set_defaults(func=database_needs_initialization)
    command_initialized = subparsers.add_parser(
        "database-initialized", help="Set the LDAP database initialization status to true / initialized"
    )
    command_initialized.set_defaults(func=database_initialized)
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level.upper())

    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()

    v1 = client.CoreV1Api()

    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
        namespace = f.read()
    logger.debug("Namespace: %s" % namespace)

    args.func(v1, namespace)


if __name__ == "__main__":
    main()

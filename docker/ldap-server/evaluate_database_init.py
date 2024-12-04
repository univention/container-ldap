#!/usr/bin/python
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import sys

from kubernetes import client, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_configmap():
    """
    Check if the ConfigMap exists and has the key ldap_database_initialized set to true.

    Returns:
        0: Database needs initialization: ConfigMap does not exist or ldap_database_initialized is set to false.
        1: Database already initialized: ldap_database_initialized is already true in the ConfigMap.
        2: LDAP server should terminate: Unexpected error accessing the ConfigMap.
    """

    def needs_initialization():
        logger.info("Database needs initialization.")
        # FIXME: We could set the ConfigMap key to `true` here, but if the
        # initialization fails and the LDAP server restarts, the variable will
        # be set to true on the next evaluation. This would be wrong.
        sys.exit(0)

    def already_initialized():
        logger.info("Database already initialized.")
        sys.exit(1)

    def terminate(error):
        logger.error("Unexpected error accessing the ConfigMap.")
        logger.error(error)
        sys.exit(2)


    try:
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

        v1 = client.CoreV1Api()

        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            namespace = f.read()

        # FIXME: Better name if we are not planning to use it in the future.
        # Something like ldap-database-status or similar.
        # Or even make it configurable via an environment variable.
        configmap_name = "nubus-deployment-status"
        database_initialized_key = "ldap_database_initialized"

        try:
            configmap = v1.read_namespaced_config_map(
                name=configmap_name,
                namespace=namespace
            )

            if database_initialized_key not in configmap.data:
                logger.info("ConfigMap does not contain the key `%s`." % database_initialized_key)
                # FIXME: Should we terminate with 2 if the key is not present?
                # To notify an operator that the ConfigMap is not correctly configured.
                needs_initialization()

            if configmap.data[database_initialized_key].lower() == 'true':
                already_initialized()
            else:
                needs_initialization()

        except client.exceptions.ApiException as e:
            if e.status == 404:
                logger.info("ConfigMap does not exist.")
                needs_initialization()
            else:
                terminate(e)

    except Exception as e:
        terminate(e)

if __name__ == "__main__":
    check_configmap()

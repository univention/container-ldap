#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from typing import Annotated, Optional
import logging
import sys

from kubernetes import client, config
import typer

logger = logging.getLogger(__name__)

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_enable=False,
)

CONFIGMAP_NAME = "nubus-deployment-status"
DATABASE_INITIALIZED_KEY = "ldap_database_initialized"

settings = {}


@app.command()
def database_needs_initialization():
    """
    Check if the ConfigMap exists and has the key ldap_database_initialized set to true.

    Returns:
        0: Database needs initialization: ldap_database_initialized is set to false.
        1: Database already initialized: ldap_database_initialized is already true in the ConfigMap.
        2: LDAP server should terminate: Unexpected error accessing or parsing the ConfigMap.
    """

    namespace = settings["namespace"]
    v1 = client.CoreV1Api()
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


@app.command()
def database_initialized():
    namespace = settings["namespace"]
    v1 = client.CoreV1Api()
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


@app.callback()
def prepare_app(
    namespace: Annotated[
        Optional[str],
        typer.Option(
            help="Kubernetes namespace to lookup the status configmap.",
        ),
    ] = None,
    log_level: Annotated[
        str,
        typer.Option(
            help="Set the log level."
        ),
    ] = "info",
):
    logging.basicConfig(level=log_level.upper())

    configure_kubernetes_client()

    if not namespace:
        namespace = discover_namespace()

    settings["namespace"] = namespace
    logger.debug("Namespace: %s" % namespace)


def configure_kubernetes_client():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()


def discover_namespace():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
        namespace = f.read()
    return namespace


if __name__ == "__main__":
    app()

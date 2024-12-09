#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from enum import Enum
from typing import Annotated, Optional
import logging
import sys

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from pydantic import BaseModel
import typer

logger = logging.getLogger(__name__)

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_enable=False,
)

DATABASE_INITIALIZED_KEY = "ldap_database_initialized"

settings = {}


class InitializedEnum(str, Enum):
    INITIALIZED = "initialized"
    UNINITIALIZED = "uninitialized"


class LdapStatus(BaseModel):
    ldap_database_initialized: InitializedEnum


@app.command()
def database_needs_initialization():
    """
    Check if the ConfigMap exists and has the key ldap_database_initialized set to true.

    Returns:
        0: Database needs initialization: ldap_database_initialized is set to false.
        1: Database already initialized: ldap_database_initialized is already true in the ConfigMap.
        2: LDAP server should terminate: Unexpected error accessing or parsing the ConfigMap.
    """
    try:
        try:
            configmap = get_validated_configmap()
        except ApiException as exc:
            if exc.status == 404:
                configmap = create_configmap()
            else:
                raise
        if configmap.data[DATABASE_INITIALIZED_KEY].lower() == InitializedEnum.INITIALIZED:
            logger.info("Database already initialized.")
            sys.exit(1)
    except Exception:
        logger.exception("Unexpected error evaluating the database initialization status.")
        sys.exit(2)

    logger.info("Database needs initialization.")


@app.command()
def database_initialized():
    """
    Update the status ConfigMap to flag the LDAP database as initialized.
    """
    configmap_name = settings["configmap"]
    namespace = settings["namespace"]
    v1 = client.CoreV1Api()
    try:
        configmap = get_validated_configmap()
        configmap.data[DATABASE_INITIALIZED_KEY] = InitializedEnum.INITIALIZED
        v1.replace_namespaced_config_map(name=configmap_name, namespace=namespace, body=configmap)
    except Exception:
        logger.exception("Unexpected error updating the database initialization status.")
        sys.exit(2)

    logger.info("Database initialization status set to true in the %s ConfigMap", configmap_name)


@app.callback()
def prepare_app(
    configmap: Annotated[
        str,
        typer.Option(
            envvar="STATUS_CONFIGMAP",
            help="Name of the status ConfigMap.",
        ),
    ],
    namespace: Annotated[
        Optional[str],
        typer.Option(
            envvar="STATUS_NAMESPACE",
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
    configure_logging(log_level)
    configure_kubernetes_client()

    if not namespace:
        namespace = discover_namespace()

    settings.update({
        "configmap": configmap,
        "namespace": namespace,
    })

    logger.debug("Configuration: %s", settings)


def create_configmap():
    configmap_name = settings["configmap"]
    namespace = settings["namespace"]
    v1 = client.CoreV1Api()
    body = {
        "api_version": "v1",
        "metadata": {
            "name": configmap_name,
        },
        "data": {
            DATABASE_INITIALIZED_KEY: InitializedEnum.UNINITIALIZED,
        },
    }
    result = v1.create_namespaced_config_map(namespace=namespace, body=body)
    return result


def get_validated_configmap():
    configmap_name = settings["configmap"]
    namespace = settings["namespace"]
    v1 = client.CoreV1Api()
    configmap = v1.read_namespaced_config_map(name=configmap_name, namespace=namespace)

    try:
        LdapStatus.model_validate(configmap.data)
    except:
        logger.exception("Validation of the status ConfigMap did fail")
        raise

    return configmap


def configure_logging(log_level):
    logging.basicConfig(level=log_level.upper())


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

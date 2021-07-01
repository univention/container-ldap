#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Vars lib for gitlab-ci"""

# included
import os

DEFAULT_UPX_IMAGE_REGISTRY = 'artifacts.knut.univention.de/upx/'

DEFAULT_QUAY_IMAGE_REGISTRY = 'quay.io/univention/'

DEFAULT_CI_PIPELINE_ID = 'none'

MINIMAL_DOCKER_VARS = ['DOCKER_HOST']

ADDITIONAL_PULL_PUSH_VARS = (
    'DBUS_SESSION_BUS_ADDRESS',
    'PATH',
)

ADDITIONAL_COMPOSE_VARS = (
    'CI_COMMIT_SHA',
    'CI_JOB_STARTED_AT',
    'CI_PIPELINE_ID',
    'CI_PROJECT_URL',
    'DBUS_SESSION_BUS_ADDRESS',
    'LANG',
    'PWD',
)

DEFAULT_DOCKER_COMPOSE_BUILD_FILES = (
    '--file docker-compose.yaml'
    ' --file docker-compose.override.yaml'
    ' --file docker-compose.prod.yaml'
)


def get_env_vars(var_names):
    """Check for environmental variables and return them as a dict"""
    return {
        var_name: os.environ[var_name]
        for var_name in var_names if var_name in os.environ
    }


# [EOF]

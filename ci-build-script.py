#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""Build script for gitlab-ci"""

# included
import os
import sys

# third party
import sh  # pylint: disable=import-error

sh2 = sh(_out='/dev/stdout', _err='/dev/stderr')  # pylint: disable=not-callable

MANDATORY_ENV_VARS = (
    'CI_PIPELINE_TAG',
    'DOCKER_COMPOSE_BUILD_FILES',
    'UPX_IMAGE_REGISTRY',
)


class AppVersionNotFound(Exception):
    """Raised if /version file could not be read"""


def add_version_label(image_name):
    """Adds a version label to an image"""
    print('Retrieving /version from {}'.format(image_name))
    result = sh2.docker.run(
        '--rm',
        '--entrypoint=/bin/cat',
        image_name,
        '/version',
        _out=None,
    ).stdout
    app_version = result.rstrip().decode('ascii')
    if not app_version:
        raise AppVersionNotFound
    print('Adding version label {}'.format(app_version))
    sh2.docker.build(
        '--label',
        'org.opencontainers.app.version={}'.format(app_version),
        '--tag',
        image_name,
        '-',
        _in='FROM {}'.format(image_name),
    )
    print('Done with labeling')


def main():
    """The main script builds, labels and pushes"""
    for env_var_name in MANDATORY_ENV_VARS:
        if env_var_name not in os.environ:
            print('Please define "{}"!'.format(env_var_name))
            return 1

    docker_compose_build_files = os.environ['DOCKER_COMPOSE_BUILD_FILES']
    upx_image_registry = os.environ['UPX_IMAGE_REGISTRY']
    ci_pipeline_tag = os.environ['CI_PIPELINE_TAG']

    sh2.cp('.env.ldap-server.example', '.env.ldap-server')
    sh2.docker_compose(
        docker_compose_build_files.split(),
        'build',
        '--parallel',
    )

    image_name = '{}ldap/notifier:{}test'.format(
        upx_image_registry, ci_pipeline_tag
    )
    try:
        add_version_label(image_name)
    except AppVersionNotFound:
        return 2

    image_name = '{}ldap/server:{}test'.format(
        upx_image_registry, ci_pipeline_tag
    )
    try:
        add_version_label(image_name)
    except AppVersionNotFound:
        return 3

    sh2.docker_compose(
        docker_compose_build_files.split(),
        'push',
    )

    return 0


if __name__ == '__main__':
    sys.exit(main())

# [EOF]

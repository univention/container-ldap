#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""Build script for gitlab-ci"""

# included
import os
import sys
import time

# third party
import sh  # pylint: disable=import-error

# internal imports
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LIBS_DIR = os.path.join(BASE_DIR, 'lib')
sys.path.insert(1, LIBS_DIR)

import ci_docker  # noqa: E402,E501; pylint: disable=import-error,wrong-import-position
from ci_log import (  # noqa: E402,E501; pylint: disable=import-error,wrong-import-position
    log,
)
import ci_vars  # noqa: E402; pylint: disable=import-error,wrong-import-position
import ci_version  # noqa: E402,E501; pylint: disable=import-error,wrong-import-position

# pylint: disable=not-callable
sh_noout = sh(_cwd=BASE_DIR)

# pylint: disable=not-callable
sh_out = sh(_out='/dev/stdout', _err='/dev/stderr', _cwd=BASE_DIR)


def main(service):  # pylint: disable=too-many-locals
    """The main script builds, labels and pushes"""

    docker_env = ci_vars.get_env_vars(ci_vars.MINIMAL_DOCKER_VARS)

    pull_push_env = ci_vars.get_env_vars(ci_vars.ADDITIONAL_PULL_PUSH_VARS)
    pull_push_env.update(docker_env)

    compose_env = {
        'COMPOSE_DOCKER_CLI_BUILD': '0',
        'CI_PROJECT_URL': 'unset',
        'CI_PIPELINE_ID': ci_vars.DEFAULT_CI_PIPELINE_ID,
        'LANG': 'C.UTF-8',
    }

    if 'CI_JOB_STARTED_AT' not in os.environ:
        compose_env['CI_JOB_STARTED_AT'] = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
        )

    if 'CI_COMMIT_SHA' not in os.environ:
        # pylint: disable=too-many-function-args
        compose_env['CI_COMMIT_SHA'] = (
            sh_noout.git('rev-parse', 'HEAD').stdout.rstrip().decode('ascii')
        )

    compose_env.update(ci_vars.get_env_vars(ci_vars.ADDITIONAL_COMPOSE_VARS))
    compose_env.update(docker_env)

    docker_compose_build_files = os.environ.get(
        'DOCKER_COMPOSE_BUILD_FILES',
        ci_vars.DEFAULT_DOCKER_COMPOSE_BUILD_FILES,
    )

    ci_pipeline_id = compose_env['CI_PIPELINE_ID']

    upx_image_registry = os.environ.get(
        'UPX_IMAGE_REGISTRY',
        ci_vars.DEFAULT_UPX_IMAGE_REGISTRY,
    )

    sh_out.cp('.env.ldap-server.example', '.env.ldap-server')
    sh_out.docker_compose(
        docker_compose_build_files.split(),
        'build',
        service if service else '--parallel',
        _env=compose_env,
    )

    services = ('notifier', 'server')
    if service:
        services = (service, )
    for cur_service in services:
        image_path = '{}ldap/{}'.format(upx_image_registry, cur_service)

        try:
            ci_docker.add_and_push_build_version_label_and_tag(
                image_path,
                ci_pipeline_id,
                docker_env,
                pull_push_env,
            )
        except ci_version.AppVersionNotFound:
            log.error('app version not found')
            return 2

        if cur_service == 'server':
            quay_image_registry = os.environ.get(
                'QUAY_IMAGE_REGISTRY',
                ci_vars.DEFAULT_QUAY_IMAGE_REGISTRY,
            )
            quay_image_name = 'univention-upx-container-ldap-openldap'
            quay_server_path = '{}{}'.format(
                quay_image_registry, quay_image_name
            )
            build_path = '{}:build-{}'.format(image_path, ci_pipeline_id)
            app_version = ci_version.get_app_version(build_path, docker_env)
            clean_version = ci_version.cleanup_for_docker_tag(app_version)
            tag = '{}:{}-{}'.format(
                quay_server_path, clean_version, ci_pipeline_id
            )
            ci_docker.add_and_push_tag(
                build_path, tag, docker_env, pull_push_env
            )

    # push tag "build-<ci-pipeline-id>"
    args = [
        docker_compose_build_files.split(),
        'push',
    ]
    if service:
        args.append(service)
    sh_out.docker_compose(
        *args,
        _env=compose_env,
    )

    return 0


if __name__ == '__main__':
    SERVICE = ''
    if len(sys.argv) > 1:
        SERVICE = sys.argv[1]
    sys.exit(main(SERVICE))

# [EOF]

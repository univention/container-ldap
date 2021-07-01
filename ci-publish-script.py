#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""Build script for gitlab-ci"""

# included
import os
import sys

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
sh_out = sh(_out='/dev/stdout', _err='/dev/stderr', _cwd=BASE_DIR)


def add_and_push_version_tag(
    image_path, ci_pipeline_id, docker_env, pull_push_env, push_path
):
    """Get the version, push latest and version tags"""
    build_path = '{}:build-{}'.format(image_path, ci_pipeline_id)

    try:
        sh_out.docker.pull(build_path, _env=pull_push_env)
    # pylint: disable=no-member
    except sh.ErrorReturnCode_1 as docker_pull_failed:
        raise ci_docker.DockerPullFailed from docker_pull_failed

    app_version = ci_version.get_app_version(build_path, docker_env)

    tag = '{}:latest'.format(push_path)
    # push tag "latest"
    ci_docker.add_and_push_tag(build_path, tag, docker_env, pull_push_env)

    clean_version = ci_version.cleanup_for_docker_tag(app_version)
    tag = '{}:{}'.format(push_path, clean_version)
    # push tag "<version>"
    ci_docker.add_and_push_tag(build_path, tag, docker_env, pull_push_env)


def main():
    """The main script builds, labels and pushes"""

    docker_env = ci_vars.get_env_vars(ci_vars.MINIMAL_DOCKER_VARS)

    pull_push_env = ci_vars.get_env_vars(ci_vars.ADDITIONAL_PULL_PUSH_VARS)
    pull_push_env.update(docker_env)

    ci_pipeline_id = os.environ.get(
        'CI_PIPELINE_ID', ci_vars.DEFAULT_CI_PIPELINE_ID
    )

    upx_image_registry = os.environ.get(
        'UPX_IMAGE_REGISTRY',
        ci_vars.DEFAULT_UPX_IMAGE_REGISTRY,
    )

    quay_image_registry = os.environ.get(
        'QUAY_IMAGE_REGISTRY',
        ci_vars.DEFAULT_QUAY_IMAGE_REGISTRY,
    )

    upx_notifier_path = '{}ldap/notifier'.format(upx_image_registry)
    upx_server_path = '{}ldap/server'.format(upx_image_registry)
    quay_server_path = '{}univention-upx-container-ldap-openldap'.format(
        quay_image_registry
    )

    targets = (
        (upx_notifier_path, upx_notifier_path),
        (upx_server_path, upx_server_path),
        (upx_server_path, quay_server_path),
    )

    for (image_path, push_path) in targets:
        try:
            add_and_push_version_tag(
                image_path,
                ci_pipeline_id,
                docker_env,
                pull_push_env,
                push_path,
            )
        except ci_version.AppVersionNotFound:
            log.error('app version not found')
            return 2
        except ci_docker.DockerPullFailed:
            log.error('dock pull failed')
            return 1
        except ci_docker.DockerPushFailed:
            log.error('dock push failed')
            return 3

    return 0


if __name__ == '__main__':
    sys.exit(main())

# [EOF]

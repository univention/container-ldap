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


def main(service):
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

    services = ('notifier', 'server')
    if service:
        services = (service, )
    for cur_service in services:
        image_path = '{}ldap/{}'.format(upx_image_registry, cur_service)
        push_paths = [image_path]
        if cur_service == 'server':
            quay_image_registry = os.environ.get(
                'QUAY_IMAGE_REGISTRY',
                ci_vars.DEFAULT_QUAY_IMAGE_REGISTRY,
            )
            quay_image_name = 'univention-upx-container-ldap-openldap'
            quay_server_path = '{}{}'.format(
                quay_image_registry, quay_image_name
            )
            push_paths.append(quay_server_path)
        for push_path in push_paths:
            try:
                ci_docker.pull_add_push_publish_version_tag(
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
                log.error('docker push failed')
                return 3

    return 0


if __name__ == '__main__':
    SERVICE = ''
    if len(sys.argv) > 1:
        SERVICE = sys.argv[1]
    sys.exit(main(SERVICE))

# [EOF]

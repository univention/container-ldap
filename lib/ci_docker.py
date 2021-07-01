#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Docker lib for gitlab-ci"""

# included
import os

# third party
import sh  # pylint: disable=import-error

# internal imports
from ci_log import log

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# pylint: disable=not-callable
sh_out = sh(_out='/dev/stdout', _err='/dev/stderr', _cwd=BASE_DIR)


class DockerPullFailed(Exception):
    """Raised if docker pull fails"""


class DockerPushFailed(Exception):
    """Raised if docker pull fails"""


def add_and_push_tag(image_name, tag, docker_env, pull_push_env):
    """Adds a tag to an image"""
    log.info('Adding tag {} to {}', tag, image_name)
    sh_out.docker.tag(image_name, tag, _env=docker_env)
    try:
        sh_out.docker.push(tag, _env=pull_push_env)
    # pylint: disable=no-member
    except sh.ErrorReturnCode_1 as docker_pull_failed:
        raise DockerPushFailed from docker_pull_failed
    log.info('Done with this tag')


# [EOF]

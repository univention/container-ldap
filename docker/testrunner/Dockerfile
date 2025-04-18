# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=0.16.2-build-2025-04-17@sha256:2614ac0157b519e0ee8cb77865aef8df5f103dbc5d4245ac99f61a0abfb94516
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/components/ucs-base-image/ucs-base-520

ARG WORKDIR="/app"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} as build
ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
      python3-pip \
      libldap2-dev \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV \
    WEB_CONCURRENCY=1 \
    # Do not buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Do not create `.pyc` files
    PYTHONDONTWRITEBYTECODE=1 \
    # Do not exceed connection pool
    POETRY_INSTALLER_MAX_WORKERS=5 \
    # Do not ask questions
    POETRY_NO_INTERACTION=1 \
    # Put .venv inside source folder
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # Cache of poetry
    POETRY_CACHE_DIR=/tmp/poetry_cache

# install Poetry
RUN pip3 install --break-system-packages --no-cache-dir poetry==1.6.1

# copy source code
COPY ./univention ${WORKDIR}/univention/
COPY ./tests ${WORKDIR}/tests/
COPY poetry.lock \
     pyproject.toml \
     ${WORKDIR}/

# install dependencies
RUN poetry install --with dev

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.2-build.20250821@sha256:839b93e89298c51a9c8cd45c119a284f9161b18d7270da4dc92588772ca20f4d
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base


ARG WORKDIR="/app"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} as build
ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apt-get -qq update \
  && apt-get --assume-yes --verbose-versions --no-install-recommends install \
  python3-pip \
  build-essential \
  python3-dev \
  libldap2-dev \
  libsasl2-dev \
  && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*
ENV \
  PATH="/root/.local/bin:${PATH}" \
  PYTHONPATH="." \
  WEB_CONCURRENCY=1 \
  # Do not buffer `stdout`
  PYTHONUNBUFFERED=1 \
  # Do not create `.pyc` files
  PYTHONDONTWRITEBYTECODE=1 \
  # Do not ask questions
  POETRY_NO_INTERACTION=1 \
  # Put .venv inside source folder
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  # Cache of poetry
  POETRY_CACHE_DIR=/tmp/poetry_cache

# install Poetry
RUN pip3 install --break-system-packages --no-cache-dir poetry==1.6.1

# copy source code
COPY ./poetry.lock \
  ./pyproject.toml \
  ${WORKDIR}/
COPY ./univention ${WORKDIR}/univention

# install dependencies
RUN poetry install --only main

###############################################
# Stage 2: final image
FROM build as final
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=build ${WORKDIR} ${WORKDIR}

ENTRYPOINT [".venv/bin/python3", "-m", "univention.ldif_producer"]

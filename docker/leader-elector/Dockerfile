# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261008@sha256:52175e1efb9452119ed135126afd931d4e2361bdc69bded46101e35fa27ae0d0
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

ARG WORKDIR="/app"
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    python3-pip \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV \
    PYTHONPATH="." \
    # Do not buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Do not create `.pyc` files
    PYTHONDONTWRITEBYTECODE=1

RUN pip3 install --break-system-packages --no-cache-dir \
    kubernetes==31.* \
    pydantic-settings==2.6.1

COPY ./leader_elector.py ${WORKDIR}/

###############################################
# Stage 2: final image
FROM build AS final
ARG WORKDIR
WORKDIR ${WORKDIR}
COPY --from=build ${WORKDIR} ${WORKDIR}

USER 1000:1000
CMD ["./leader_elector.py"]

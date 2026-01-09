# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.4-build.20260108@sha256:97b04d50531636aa2e30e915b38e3daacea1e49b58774daa97f9d698e6855a93
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

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261119@sha256:f5810786b9a4ed68f05cd8ecbd6fe547d241717ae855cf397ac57587603a2ab1
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_DISTROLESS_IMAGE_TAG=5.3.0-build.20261119@sha256:eff017317b60195fd2881f16644461bb3b90bddbecb2c9772d20e06bd2128828
ARG UCS_DISTROLESS_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-distroless-python

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /usr/local/bin/uv

# The venv has to use the system CPython, which the distroless image provides at the same path.
ENV UV_PYTHON_DOWNLOADS=never

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev


FROM ${UCS_DISTROLESS_IMAGE}:${UCS_DISTROLESS_IMAGE_TAG} AS final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=build --chown=1000:1000 /app/.venv /app/.venv
COPY --chown=1000:1000 leader_elector.py .

RUN ["/app/.venv/bin/python", "-c", "import leader_elector"]

ENTRYPOINT ["/app/.venv/bin/python", "/app/leader_elector.py"]

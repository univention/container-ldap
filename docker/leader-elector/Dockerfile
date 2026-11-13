# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261112@sha256:25e5e183b1b4f75c64e0c697d5795a8e9c15b935453c2a64406d7d1ab40b2214
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_DISTROLESS_IMAGE_TAG=5.3.0-build.20261112@sha256:c4766a3c4624d2173f1b39da3be5088c90e64564ce0fccf14f9106ee83fb422c
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

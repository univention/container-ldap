# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261106@sha256:c59ae38f5a819046f9283904c4c64dbc9c77cf323173c44e4686db472334d184
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_DISTROLESS_IMAGE_TAG=5.3.0-build.20261106@sha256:f4e537e49d316d4a744ca7c2f11ab11936993811bf0ed76a6bd0414ed03f03bc
ARG UCS_DISTROLESS_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-distroless-python

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.6@sha256:af22a52f5eafef3d78e551599d405c02df61919d18028f0cea8eda93bc9986d0 /uv /usr/local/bin/uv

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

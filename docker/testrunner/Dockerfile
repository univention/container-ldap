ARG DOCKER_PROXY

FROM ${DOCKER_PROXY}debian:bookworm-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
        ldap-utils=2.5* \
        python3=3.11.* \
        python3-pip=23.* \
        python3-venv=3.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /testrunner

# Install python dependencies and helper scripts
COPY Pipfile Pipfile.lock entrypoint.sh ./

# hadolint ignore=SC1091
RUN python3 -m venv .venv \
    && source ./.venv/bin/activate \
    && pip install --no-cache-dir pipenv==2023.6.18 \
    && pipenv sync --dev --system \
    && rm -r ~/.cache

WORKDIR /app

ENTRYPOINT ["/testrunner/entrypoint.sh"]
CMD ["pytest"]

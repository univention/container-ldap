
# Just for later reference
FROM hadolint/hadolint:latest-alpine AS hadolint

# Create a virtualenv
FROM python:3.7-alpine AS venv

RUN \
  pip install virtualenv && \
  virtualenv /venv && \
  /venv/bin/pip install --upgrade pip

# install pre-commit and dependencies
FROM python:3.7-alpine AS final

COPY --from=hadolint \
  /bin/hadolint \
  /usr/bin/

COPY --from=venv \
  /venv \
  /venv

RUN \
  apk add --no-cache bash docker-compose gcc git musl-dev shellcheck && \
  rm -rf /var/cache/apk/* && \
  /venv/bin/pip install pre-commit && \
  rm -rf /root/.cache/pip/ && \
  mkdir /code

WORKDIR /code

CMD ["/venv/bin/pre-commit", "run", "--all-files"]

# [EOF]

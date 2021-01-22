
# Just for later reference
FROM hadolint/hadolint:latest-alpine AS hadolint

# install pre-commit and dependencies
FROM alpine:3.13 AS final

COPY --from=hadolint \
  /bin/hadolint \
  /usr/bin/

RUN \
  apk add --no-cache bash git python3 \
    # Dependencies of multiple pre-commit linters:
    py3-virtualenv py3-typed-ast py3-cffi \
    py3-bcrypt py3-cryptography py3-pynacl \
    # Dependencies of github.com/pryorda/dockerfilelint-precommit-hooks
    libgcc libstdc++ \
    # Dependencies of github.com/detailyang/pre-commit-shell:
    shellcheck && \
  rm -rf /var/cache/apk/* && \
  wget --no-check-certificate \
    --output-document \
      /usr/local/share/ca-certificates/git.knut.univention.de.crt \
    https://billy.knut.univention.de/ucs-root-ca.crt && \
  update-ca-certificates && \
  # From now on install into virtualenv
  mkdir -p /root/.config/virtualenv/ && \
  echo -e "[virtualenv]\nsystem_site_packages = true" \
    > /root/.config/virtualenv/virtualenv.ini && \
  virtualenv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install pre-commit docker-compose && \
  rm -rf /root/.cache/pip/ && \
  mkdir /code

ENV PATH="/venv/bin/:${PATH}"

WORKDIR /code

CMD ["pre-commit", "run", "--all-files"]

# [EOF]

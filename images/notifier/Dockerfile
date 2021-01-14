###############################################################################
# Dockerfile for the univention-directory-notifier

ARG DEBIAN_BASE_IMAGE_TAG=buster-slim

FROM debian:${DEBIAN_BASE_IMAGE_TAG} AS build

ARG APT_KEY_URL=https://updates.software-univention.de/univention-archive-key-ucs-5x.gpg

# Ignore questions from debconf
ARG DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

###############################################################################
# Install Univention APT-Key

RUN \
  set -euxo pipefail && \
  apt-get update && \
  apt-get --assume-yes --verbose-versions --no-install-recommends install \
    ca-certificates curl gpg gpg-agent && \
  curl -fsSL "${APT_KEY_URL}" | apt-key add - && \
  rm -rf /var/lib/apt/lists/*

###############################################################################
# Install univention-directory-notifier

COPY sources.list /etc/apt/sources.list.d/15_ucs-online-version.list

# TODO: remove nameserver after public release
RUN \
  set -euxo pipefail && \
  echo 'nameserver 192.168.0.97' > /etc/resolv.conf && \
  apt-get update && \
  apt-get --assume-yes --verbose-versions --no-install-recommends install \
    univention-directory-notifier && \
  rm -rf /var/lib/apt/lists/*

###############################################################################
# Second stage image to get rid of unneeded files

FROM debian:${DEBIAN_BASE_IMAGE_TAG} AS final

# Copy dependencies for univention-directory-notifier
# libssl1.1: libcrypto.so.1.1
# libldap-2.4-2: liblber-2.4.so.2 libldap_r-2.4.so.2
# libsasl2-2: libsasl2.so.2
# libssl1.1: libssl.so.1.1
# libunivention-debug1: libuniventiondebug.so.1
COPY --from=build \
  /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 \
  /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2 \
  /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2.10.10 \
  /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2 \
  /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.10 \
  /usr/lib/x86_64-linux-gnu/libsasl2.so.2 \
  /usr/lib/x86_64-linux-gnu/libssl.so.1.1 \
  /usr/lib/x86_64-linux-gnu/libuniventiondebug.so.1 \
  /usr/lib/x86_64-linux-gnu/libuniventiondebug.so.1.0.0 \
  /usr/lib/x86_64-linux-gnu/

# Copy translog import script
# univention-directory-notifier
COPY --from=build \
  /usr/share/univention-directory-notifier/univention-translog \
  /usr/share/univention-directory-notifier/

# Copy daemon watching /var/lib/univention-ldap/listener/listener
# univention-directory-notifier
COPY --from=build \
  /usr/sbin/univention-directory-notifier \
  /usr/sbin/univention-directory-notifier

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

CMD [ \
  "-d 1", \
  "-v 3", \
  "-F" \
]

# [EOF]

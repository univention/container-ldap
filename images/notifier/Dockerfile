###############################################################################
# Dockerfile for the univention-directory-notifier

ARG DOCKERHUB_CACHE=artifacts.knut.univention.de/dockerhub_proxy_cache/library/
ARG DEBIAN_BASE_IMAGE_TAG=buster-slim

FROM ${DOCKERHUB_CACHE}debian:${DEBIAN_BASE_IMAGE_TAG} AS build

ARG APT_KEY_URL=https://updates.software-univention.de/univention-archive-key-ucs-5x.gpg

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

WORKDIR /apt

###############################################################################
# Install Univention APT-Key

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get --assume-yes --verbose-versions --no-install-recommends install \
      ca-certificates=20* \
      curl=7.64.* \
      gpg=2.2.* \
      gpg-agent=2.2.* \
      patch=2.7.* \
  && \
  curl -fsSL "${APT_KEY_URL}" | apt-key add - && \
  rm -rf /var/lib/apt/lists/*


###############################################################################
# Install univention-directory-notifier

COPY sources.list /etc/apt/sources.list.d/15_ucs-online-version.list

# The following scripts get called during dpkg-install but are not required
# in a container environment
COPY fake.sh /usr/local/bin/call_joinscript
COPY fake.sh /usr/local/bin/create_logfile
COPY fake.sh /usr/local/bin/ucr
COPY fake.sh /usr/local/bin/systemctl
COPY fake.sh /usr/local/bin/univention-config-registry

COPY patches/ /patches/

# TODO: remove nameserver after public release
RUN \
  echo 'nameserver 192.168.0.97' > /etc/resolv.conf && \
  apt-get update && \
  apt-get download \
    libldap-2.4-2=2.4.* \
    libsasl2-2=2.1.* \
    libssl1.1=1.1.* \
    libunivention-debug1=12.0.* \
    python-ldap=3.1.* \
    python-univention-config-registry=15.0.* \
    python-univention-debhelper=2.0.* \
    python-six=1.12.* \
    univention-directory-notifier=14.0.* && \
  mkdir /usr/share/univention-lib/ && \
  # The original file would source many bash-helper-functions not required here.
  touch /usr/share/univention-lib/all.sh && \
  dpkg --install --force-depends /apt/* && \
  patch --directory=/ --strip=0 < /patches/translog-py3.patch && \
  rm -rf /apt /patches /var/lib/apt/lists/* && \
  awk \
    '/^Package: univention-directory-notifier$/{ while(!/^Version: /){getline} print $2 }' \
    /var/lib/dpkg/status > /version


###############################################################################
# Second stage image to get rid of unneeded files

FROM ${DOCKERHUB_CACHE}debian:${DEBIAN_BASE_IMAGE_TAG} AS final

ARG LABEL_CREATED=undefined
ARG LABEL_REVISION=undefined
ARG LABEL_SOURCE=undefined
ARG LABEL_VERSION=undefined

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

# Copy python-ldap and python-six dependencies for univention-translog
COPY --from=build \
  /usr/lib/python2.7/dist-packages/_ldap.x86_64-linux-gnu.so \
  /usr/lib/python2.7/dist-packages/ldap/ \
  /usr/lib/python2.7/dist-packages/six.py \
  /usr/lib/python2.7/dist-packages/

# Copy python-univention-config-registry dependency for univention-translog
COPY --from=build \
  /usr/lib/python2.7/dist-packages/univention/config_registry/ \
  /usr/lib/python2.7/dist-packages/univention/config_registry/

# Copy debhelper dependency for univention-translog
COPY --from=build \
  /usr/lib/python2.7/dist-packages/univention/debhelper.py \
  /usr/lib/python2.7/dist-packages/univention/debhelper.py

# Copy dependencies for univention-directory-notifier
# libldap-2.4-2: liblber-2.4.so.2.10.10 libldap_r-2.4.so.2.10.10
# libsasl2-2: libsasl2.so.2.0.25
# libcrypto.so.1.1 and libssl.so.1.1 from libssl1.1
# libuniventiondebug.so.1.0.0 from libunivention-debug1
COPY --from=build \
  # from libssl1.1
  /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 \
  # from libldap-2.4-2
  /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2.10.* \
  # from libldap-2.4-2
  /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.* \
  # from libsasl2-2
  /usr/lib/x86_64-linux-gnu/libsasl2.so.2.0.* \
  # from libssl1.1
  /usr/lib/x86_64-linux-gnu/libssl.so.1.1 \
  # from libunivention-debug1
  /usr/lib/x86_64-linux-gnu/libuniventiondebug.so.1.0.* \
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

COPY --from=build \
  /version \
  /version

# TODO: remove log-dir, when log-to-stdout has been released
#   https://forge.univention.org/bugzilla/show_bug.cgi?id=52716
RUN \
  # Needed to help Python find the config_registry module in there.
  touch /usr/lib/python2.7/dist-packages/univention/__init__.py && \
  # Needed because the notifier creates its log-file in there.
  mkdir /var/log/univention/ && \
  SRC=$(find /usr/lib/x86_64-linux-gnu -type f -name 'liblber-2.4.so.2.*' -printf "%f") && \
  ln --symbolic \
    "${SRC}" \
    /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2 && \
  SRC=$(find /usr/lib/x86_64-linux-gnu -type f -name 'libldap_r-2.4.so.2.*' -printf "%f") && \
  ln --symbolic \
    "${SRC}" \
    /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2 && \
  SRC=$(find /usr/lib/x86_64-linux-gnu -type f -name 'libsasl2.so.2.*' -printf "%f") && \
  ln --symbolic \
    "${SRC}" \
    /usr/lib/x86_64-linux-gnu/libsasl2.so.2 && \
  SRC=$(find /usr/lib/x86_64-linux-gnu -type f -name 'libuniventiondebug.so.1.*' -printf "%f") && \
  ln --symbolic \
    "${SRC}" \
    /usr/lib/x86_64-linux-gnu/libuniventiondebug.so.1 && \
  ln --symbolic \
    /dev/stdout \
    /var/log/univention/notifier.log

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

# Parameters for univention-directory-notifier
CMD [ \
  "-d 4", \
  "-v 3", \
  "-F" \
]

LABEL org.opencontainers.image.created="${LABEL_CREATED}"
LABEL org.opencontainers.image.description="Univention LDAP Notifier"
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"
LABEL org.opencontainers.image.revision="${LABEL_REVISION}"
LABEL org.opencontainers.image.source="${LABEL_SOURCE}"
LABEL org.opencontainers.image.title="ldap/notifier"
LABEL org.opencontainers.image.url="https://docs.software-univention.de/manual-5.0.html#introduction:Listener_notifier_replication"
LABEL org.opencontainers.image.vendor="Univention GmbH"
LABEL org.opencontainers.image.version="${LABEL_VERSION}"

# [EOF]

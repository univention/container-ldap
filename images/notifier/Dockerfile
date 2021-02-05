###############################################################################
# Dockerfile for the univention-directory-notifier

ARG DEBIAN_BASE_IMAGE_TAG=buster-slim

FROM debian:${DEBIAN_BASE_IMAGE_TAG} AS build

ARG APT_KEY_URL=https://updates.software-univention.de/univention-archive-key-ucs-5x.gpg

# Ignore questions from debconf
ARG DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

WORKDIR /apt

###############################################################################
# Install Univention APT-Key

RUN \
  apt-get update && \
  apt-get --assume-yes --verbose-versions --no-install-recommends install \
    ca-certificates=20200601~deb10u2 \
    curl=7.64.0-4+deb10u1 \
    gpg=2.2.12-1+deb10u1 \
    gpg-agent=2.2.12-1+deb10u1 && \
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

# TODO: remove nameserver after public release
RUN \
  echo 'nameserver 192.168.0.97' > /etc/resolv.conf && \
  apt-get update && \
  apt-get download \
    libldap-2.4-2=2.4.47+dfsg-3+deb10u4A~5.0.0.202102022256 \
    libsasl2-2=2.1.27+dfsg-1+deb10u1 \
    libssl1.1=1.1.1d-0+deb10u4 \
    libunivention-debug1=12.0.1-1A~5.0.0.202102041003 \
    python-ldap=3.1.0-2A~5.0.0.202011181801 \
    python-univention-config-registry=15.0.6-2A~5.0.0.202101211116 \
    python-univention-debhelper=2.0.0-3A~5.0.0.202010151132 \
    python-six=1.12.0-1 \
    univention-directory-notifier=14.0.4-4A~5.0.0.202012141233 && \
  mkdir /usr/share/univention-lib/ && \
  # The original file would source many bash-helper-functions not required here.
  touch /usr/share/univention-lib/all.sh && \
  dpkg --install --force-depends /apt/* && \
  rm -rf /apt /var/lib/apt/lists/*

###############################################################################
# Second stage image to get rid of unneeded files

FROM debian:${DEBIAN_BASE_IMAGE_TAG} AS final

SHELL ["/bin/bash", "-c"]

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
  /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2.10.10 \
  # from libldap-2.4-2
  /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.10 \
  # from libsasl2-2
  /usr/lib/x86_64-linux-gnu/libsasl2.so.2.0.25 \
  # from libssl1.1
  /usr/lib/x86_64-linux-gnu/libssl.so.1.1 \
  # from libunivention-debug1
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

# TODO: remove log-dir, when log-to-stdout has been released
#   https://forge.univention.org/bugzilla/show_bug.cgi?id=52716
RUN \
  # Needed to help Python find the config_registry module in there.
  touch /usr/lib/python2.7/dist-packages/univention/__init__.py && \
  # Needed because the notifier creates its log-file in there.
  mkdir /var/log/univention/ && \
  ln --symbolic \
    liblber-2.4.so.2.10.10 \
    /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2 && \
  ln --symbolic \
    libldap_r-2.4.so.2.10.10 \
    /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2 && \
  ln --symbolic \
    libsasl2.so.2.0.25 \
    /usr/lib/x86_64-linux-gnu/libsasl2.so.2 && \
  ln --symbolic \
    libuniventiondebug.so.1.0.0 \
    /usr/lib/x86_64-linux-gnu/libuniventiondebug.so.1

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

# Parameters for univention-directory-notifier
CMD [ \
  "-d 1", \
  "-v 3", \
  "-F" \
]

# [EOF]

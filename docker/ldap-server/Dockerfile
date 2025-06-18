# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2025 Univention GmbH


###############################################################################
# Global variables
###############################################################################

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-522
ARG UCS_BASE_IMAGE_TAG=0.18.2-build-2025-06-12

###############################################################################
# Builder image for collecting Univention LDAP schema templates, base LDIFs
# and certain libraries that are maintained by Univention for UCS
# like cy2-saml
###############################################################################

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS ucs_builder

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

###############################################################################
# Install univention-ldap-server
###############################################################################

WORKDIR /home/deb_packages


RUN apt-get download \
    # The Self-service does not have an extension package. It's part of the UMC.
    # We bake support for it directly into the LDAP server image.
    univention-self-service-passwordreset-umc \
    univention-ldap-config \
    univention-ldap-server \
    univention-saml-schema \
    univention-ldap-overlay-memberof \
    univention-ldap-acl-master \
    univention-management-console-server \
    liblasso3 \
    cy2-saml && \
    (dpkg --force-all -i ./*.deb || true)

###############################################################################
# Base image
###############################################################################
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS base

ARG LABEL_CREATED=undefined
ARG LABEL_REVISION=undefined
ARG LABEL_SOURCE=undefined
ARG LABEL_VERSION=undefined

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN \
    # Do the non-interactive package configuration
    # of slapd otherwise the build process would
    # stall when debconf asks for input interactively
    { \
    echo debconf debconf/frontend select Noninteractive; \
    # Administrator password
    echo slapd slapd/password1 password 'temppwd'; \
    # Confirm password:
    echo slapd slapd/password2 password 'temppwd'; \
    } | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get --assume-yes --verbose-versions --no-install-recommends install \
    # Slapd Debian dependencies, some of them could be removed later
    libltdl7 \
    libodbc1 \
    libperl5.36 \
    libwrap0 \
    psmisc \
    perl \
    lsb-base \
    # Some definitely needed slapd dependencies
    libsasl2-2 \
    libsasl2-modules \
    libsasl2-modules-db \
    libsasl2-modules-gssapi-heimdal \
    krb5-config \
    libgssapi-krb5-2 \
    libkrb5-26-heimdal \
    libkadm5srv8-heimdal \
    openssl \
    # cy2-saml dependencies
    libglib2.0-0 \
    libxmlsec1-openssl \
    # for downloading SAML metadata on startup
    wget \
    ca-certificates \
    python3 \
    python3-pip \
    pipenv && \
    # This file is a dependency of the slapd.conf templates
    mkdir -p /var/lib/univention-ldap-local/schema/id/ && \
    echo "1" >/var/lib/univention-ldap-local/schema/id/id

###############################################################################
# Copy LDAP config and libs from UCS builder image
###############################################################################
# slapd.conf templates:
COPY --from=ucs_builder /usr/share/univention-ldap/schema \
    /usr/share/univention-ldap/schema
COPY --from=ucs_builder /etc/univention/templates/files/etc/ldap/slapd.conf.d \
    /etc/univention/templates/files/etc/ldap/slapd.conf.d
# This "info" file is also a dependency of the templates
COPY --from=ucs_builder /etc/univention/templates/info/univention-ldap-server.info \
    /etc/univention/templates/info/univention-ldap-server.info

# LDIF Files:
COPY --from=ucs_builder /usr/share/univention-ldap/base.ldif \
    /usr/share/univention-ldap/base.ldif
COPY --from=ucs_builder /usr/share/univention-ldap/core-edition.ldif \
    /usr/share/univention-ldap/core-edition.ldif
COPY --from=ucs_builder /usr/share/univention-ldap/translog.ldif \
    /usr/share/univention-ldap/translog.ldif

# local-schema files:
COPY --from=ucs_builder \
    /usr/share/univention-self-service/self-service-passwordreset.schema \
    /var/lib/univention-ldap-local/local-schema/self-service-passwordreset.schema

# Configuration of the Crude SAML plugin for Cyrus SASL2:
# This template is contained by univention-management-console-server
COPY --from=ucs_builder \
    /etc/univention/templates/files/etc/ldap/sasl2/slapd.conf \
    /etc/univention/templates/files/etc/ldap/sasl2/slapd.conf

# UCS only libraries:
COPY --from=ucs_builder \
    /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
    /usr/lib/x86_64-linux-gnu/sasl2/

# Only the UCS version of this library fits as libsaml linked against this
# and otherwise dlopen(,) complains about 'undefined symbol'
COPY --from=ucs_builder /usr/lib/liblasso.so.3.15.1  /usr/lib/

# ldconfig doesn't create the following links as this directory
# is not in any config under /etc/ld.so.conf.d/
RUN ln -s /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
    /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0 \
    \
    && ln -s /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
    /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so \
    \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    slapd \
    ldap-utils \
    # Explicitly disable cn=config, so
    # slapcat defaults to reading the config from
    # /etc/ldap/slapd.conf
    # this is the current behavior in UCS 5
    && mv "/etc/ldap/slapd.d/cn=config.ldif" \
    "/etc/ldap/slapd.d/cn=config.ldif.DISABLED" \
    && mkdir /var/lib/univention-ldap \
    # Some file ownerships are explicitly changed to the user openldap with uid 100
    # in the debian installation scripts.
    # This leads to errors when running the container as any other user and needs to be reversed.
    && chown -R 100:102 /etc/ldap/

###############################################################################
# Copy LDAP index tools
###############################################################################
RUN mkdir -p /opt/univention/ldap-tools
COPY sync_ldap_indexes.py /opt/univention/ldap-tools
COPY ldap-index-statefile.json /opt/univention/ldap-tools
RUN ln -s /opt/univention/ldap-tools/sync_ldap_indexes.py /usr/bin/sync-ldap-indexes

###############################################################################
# Copy from Docker build context
###############################################################################
WORKDIR /src
COPY Pipfile Pipfile.lock ./

###############################################################################
# Test image
###############################################################################
FROM base AS pytest

RUN pipenv sync --dev --system \
    && rm -r ~/.cache

WORKDIR /src/docker/ldap-server

CMD ["pytest"]


###############################################################################
# Final image
###############################################################################
FROM base AS final

RUN pipenv sync --system \
    && rm -r ~/.cache

WORKDIR /
COPY ucr /usr/sbin/
COPY ucr_light_filter.py /usr/sbin/ucr-light-filter

COPY 40-self-service-acl.sh \
    50-entrypoint.sh \
    /entrypoint.d/

COPY evaluate_database_init.py /usr/local/bin/evaluate_database_init

CMD ["/etc/univention/run-slapd.sh"]

# Since in the classic UCS the ports 7636 and 7389 were only needed
# for avoiding conflict with Samba domain controller service
# they are not needed in this image
EXPOSE 389 636

LABEL org.opencontainers.image.created="${LABEL_CREATED}"
LABEL org.opencontainers.image.description="Univention OpenLDAP Server"
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"
LABEL org.opencontainers.image.revision="${LABEL_REVISION}"
LABEL org.opencontainers.image.source="${LABEL_SOURCE}"
LABEL org.opencontainers.image.title="upx-ldap-server"
LABEL org.opencontainers.image.url="https://docs.software-univention.de/manual-5.0.html#introduction:LDAP_directory_service"
LABEL org.opencontainers.image.vendor="Univention GmbH"
LABEL org.opencontainers.image.version="${LABEL_VERSION}"

# [EOF]

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH


###############################################################################
# Global variables
###############################################################################

ARG UCS_BASE_IMAGE_TAG=0.13.0-build-2024-06-18
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/components/ucs-base-image/ucs-base-508

ARG PORTAL_EXTENSION_IMAGE=gitregistry.knut.univention.de/univention/components/univention-portal/portal-extension
ARG PORTAL_EXTENSION_TAG=0.26.0

ARG OX_EXTENSION_IMAGE=gitregistry.knut.univention.de/univention/open-xchange/provisioning/ox-extension
ARG OX_EXTENSION_TAG=0.9.0

ARG GUARDIAN_EXTENSIONS_IMAGE=gitregistry.knut.univention.de/univention/components/authorization-engine/guardian/ums-dependencies
ARG GUARDIAN_EXTENSIONS_TAG=latest


###############################################################################
# Builder image for collecting Univention LDAP schema templates, base LDIFs
# and certain libraries that are maintained by Univention for UCS
# like cy2-saml
###############################################################################

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} as ucs_builder

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

###############################################################################
# Install univention-ldap-server
###############################################################################

WORKDIR /home/deb_packages


RUN echo "deb [trusted=yes]    http://192.168.0.10/build2/     ucs_5.0-0-bug57267-nubus-slapdsock-prepostread/all/" > /etc/apt/sources.list.d/ucs-unreleased.list \
        && echo "deb [trusted=yes]    http://192.168.0.10/build2/     ucs_5.0-0-bug57267-nubus-slapdsock-prepostread/\$(ARCH)/" >> /etc/apt/sources.list.d/ucs-unreleased.list \
        && echo "deb-src [trusted=yes] http://192.168.0.10/build2/     ucs_5.0-0-bug57267-nubus-slapdsock-prepostread/source/" >> /etc/apt/sources.list.d/ucs-unreleased.list \
    && apt-get update -o Dir::Etc::sourcelist="sources.list.d/ucs-unreleased.list" \
        -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0" \
    && apt-get download \
        univention-appcenter=9.0.* \
        univention-self-service-passwordreset-umc=5.0.* \
        univention-ldap-config=16.0.* \
        univention-ldap-server=16.0.* \
        univention-saml-schema=7.0.* \
        univention-ldap-overlay-memberof=12.0.* \
        univention-ldap-acl-master=16.0.* \
        univention-management-console-server=12.0.* \
        liblasso3=2.6.* \
        cy2-saml=1.9.* && \
    (dpkg --force-all -i ./*.deb || true)


FROM ${PORTAL_EXTENSION_IMAGE}:${PORTAL_EXTENSION_TAG} AS portal-extension
FROM ${OX_EXTENSION_IMAGE}:${OX_EXTENSION_TAG} AS ox-extension
FROM ${GUARDIAN_EXTENSIONS_IMAGE}:${GUARDIAN_EXTENSIONS_TAG} AS guardian-extensions

###############################################################################
# Final image
###############################################################################
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

ARG LABEL_CREATED=undefined
ARG LABEL_REVISION=undefined
ARG LABEL_SOURCE=undefined
ARG LABEL_VERSION=undefined

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

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
        libltdl7=2.4.* \
        libodbc1=2.3.* \
        libperl5.28=5.28.* \
        libwrap0=7.6.* \
        psmisc=23.* \
        perl=5.28.* \
        lsb-base=10.* \
        # Some definitely needed slapd dependencies
        libsasl2-2=2.1.* \
        libsasl2-modules=2.1.* \
        libsasl2-modules-db=2.1.* \
        libsasl2-modules-gssapi-heimdal=2.1.* \
        krb5-config=2.6 \
        libgssapi-krb5-2=1.* \
        libkrb5-26-heimdal=7.5.* \
        libkadm5srv8-heimdal=7.5.* \
        openssl=1.1.* \
        # cy2-saml dependencies
        libglib2.0-0=2.* \
        libxmlsec1-openssl=1.2.* \
        # for downloading SAML metadata on startup
        wget=1.20.* \
        ca-certificates=* \
        # 30 Mb extra, only needed for ucr-light-filter
        # TODO: Remove when "Config-Adapter" sidecar is ready
        python3=3.7.* && \
    # This file is a depencecy of the slapd.conf templates
    mkdir -p /var/lib/univention-ldap-local/schema/id/ && \
    echo "1" >/var/lib/univention-ldap-local/schema/id/id

###############################################################################
# Copy LDAP config and libs from UCS builder image
###############################################################################
# slapd.conf templates:
COPY --from=ucs_builder /usr/share/univention-ldap/schema \
                        /usr/share/univention-ldap/schema
COPY --from=portal-extension /plugins/ldap-schema/ \
                             /usr/lib/univention-portal/schema
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
     /usr/share/univention-appcenter/univention-app.schema \
     /var/lib/univention-ldap-local/local-schema/univention-app.schema

COPY --from=ucs_builder \
     /usr/share/univention-self-service/self-service-passwordreset.schema \
     /var/lib/univention-ldap-local/local-schema/self-service-passwordreset.schema

COPY --from=portal-extension \
     /plugins/ldap-schema/ \
     /var/lib/univention-ldap-local/local-schema/

COPY --from=ox-extension \
     /plugins/ldap-schema/oxforucs.schema \
     /var/lib/univention-ldap-local/local-schema/oxforucs.schema

COPY --from=ox-extension \
    /plugins/ldap-schema/oxforucs-extra.schema \
    /var/lib/univention-ldap-local/local-schema/oxforucs-extra.schema

COPY --from=guardian-extensions \
     /ldap/schema/guardian.schema \
     /var/lib/univention-ldap-local/local-schema/guardian.schema

# ACLs:
COPY --from=ucs_builder \
     /usr/share/univention-appcenter/66univention-appcenter_app.acl \
     /etc/univention/templates/files/etc/ldap/slapd.conf.d/

COPY --from=portal-extension \
     /plugins/ldap-acls/ \
     /etc/univention/templates/files/etc/ldap/slapd.conf.d/

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
COPY --from=ucs_builder /usr/lib/liblasso.so.3.13.0  /usr/lib/

RUN echo "deb [trusted=yes]    http://192.168.0.10/build2/     ucs_5.0-0-bug57267-nubus-slapdsock-prepostread/all/" > /etc/apt/sources.list.d/ucs-unreleased.list \
        && echo "deb [trusted=yes]    http://192.168.0.10/build2/     ucs_5.0-0-bug57267-nubus-slapdsock-prepostread/\$(ARCH)/" >> /etc/apt/sources.list.d/ucs-unreleased.list \
        && echo "deb-src [trusted=yes] http://192.168.0.10/build2/     ucs_5.0-0-bug57267-nubus-slapdsock-prepostread/source/" >> /etc/apt/sources.list.d/ucs-unreleased.list \
    && apt-get update -o Dir::Etc::sourcelist="sources.list.d/ucs-unreleased.list" \
        -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0" \
    \
    # ldconfig doesn't create this links as this directory
    # is not in any config under /etc/ld.so.conf.d/
    && ln -s /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
          /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0 \
    \
    && ln -s /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
          /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so \
    \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
        slapd=2.4.* \
        ldap-utils=2.4.* \
    && rm -rf /var/lib/apt/lists/* \
    # Explicitly disable cn=config, so
    # slapcat defaults to reading the config from
    # /etc/ldap/slapd.conf
    # this is the current behavior in UCS 5
    && mv "/etc/ldap/slapd.d/cn=config.ldif" \
       "/etc/ldap/slapd.d/cn=config.ldif.DISABLED" \
    && mkdir /var/lib/univention-ldap


###############################################################################
# Copy from Docker build context
###############################################################################
COPY ucr /usr/sbin/
COPY ucr-light-filter /usr/sbin/

COPY 40-self-service-acl.sh \
     50-entrypoint.sh \
     /entrypoint.d/

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

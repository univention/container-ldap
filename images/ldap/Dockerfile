###############################################################################
# Builder image for collecting Univention LDAP schema templates and base LDIFs
###############################################################################
ARG DEBIAN_BASE_IMAGE_TAG
ARG DEB_BUILDER_REGISTRY
ARG DEB_BUILDER_IMAGE
ARG DEB_BUILDER_TAG
FROM debian:${DEBIAN_BASE_IMAGE_TAG} as cfg_builder

COPY sources.list /etc/apt/sources.list

RUN echo 'nameserver 192.168.0.97' > /etc/resolv.conf && \
    cd "$(mktemp --directory)" && chown _apt . && \
    apt-get update && \
    apt-get download \
        univention-ldap-config \
        univention-ldap-server \
        univention-saml-schema \
        univention-virtual-machine-manager-schema \
        univention-ldap-overlay-memberof \
        univention-ldap-acl-master && \
    (dpkg --force-all -i ./*.deb || true) && \
    rm -rf /var/lib/apt/lists/*

###############################################################################
# Builder image for OpenLDAP currently in deb package
###############################################################################
FROM ${DEB_BUILDER_REGISTRY}/${DEB_BUILDER_IMAGE}:${DEB_BUILDER_TAG} \
  AS deb_builder

###############################################################################
# Final image
###############################################################################
FROM debian:${DEBIAN_BASE_IMAGE_TAG}

RUN apt-get update && \
    # Install apt-utils otherwise we can't seem to
    # do non-interactive package configuration
    apt-get install --no-install-recommends -y apt-utils && \
    \
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
    apt-get install --no-install-recommends -y \
        # Slapd Debian dependencies, some of them could be removed later
        libltdl7 \
        libodbc1 \
        libperl5.28 \
        libwrap0 \
        psmisc \
        perl \
        libmime-base64-perl \
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
        # 30 Mb extra, only needed for ucr-light-filter
        # TODO: Remove when "Config-Adapter" sidecar is ready
        python3 && \
    rm -rf /var/lib/apt/lists/* && \
    # This file is a depencecy of the slapd.conf templates
    mkdir -p /var/lib/univention-ldap/schema/id/ && \
    echo "1" >/var/lib/univention-ldap/schema/id/id

###############################################################################
# Copy from LDAP config builder image
###############################################################################
# slapd.conf templates:
COPY --from=cfg_builder /usr/share/univention-ldap/schema \
                        /usr/share/univention-ldap/schema
COPY --from=cfg_builder /etc/univention/templates/files/etc/ldap/slapd.conf.d \
                        /etc/univention/templates/files/etc/ldap/slapd.conf.d
# This "info" file is also a dependency of the templates
COPY --from=cfg_builder /etc/univention/templates/info/univention-ldap-server.info \
                        /etc/univention/templates/info/univention-ldap-server.info

# LDIF Files:
COPY --from=cfg_builder /usr/share/univention-ldap/base.ldif \
                        /usr/share/univention-ldap/base.ldif
COPY --from=cfg_builder /usr/share/univention-ldap/core-edition.ldif \
                        /usr/share/univention-ldap/core-edition.ldif
COPY --from=cfg_builder /usr/share/univention-ldap/translog.ldif \
                        /usr/share/univention-ldap/translog.ldif

###############################################################################
# Copy from OpenLDAP binary builder image
###############################################################################
COPY --from=deb_builder /root/src/debian/slapd_2.4.47+dfsg-3+deb10u4_amd64.deb \
                        /tmp/

COPY --from=deb_builder /root/src/debian/libldap-2.4-2_2.4.47+dfsg-3+deb10u4_amd64.deb \
                        /tmp/

RUN apt-get install --assume-yes --no-install-recommends \
        /tmp/slapd_*.deb /tmp/libldap-*.deb

###############################################################################
# Copy from Docker build context
###############################################################################
COPY local-schema /var/lib/univention-ldap/local-schema
COPY ucr /usr/sbin/
COPY ucr-light-filter /usr/sbin/

COPY container-entrypoint.sh /usr/local/bin

ENTRYPOINT ["container-entrypoint.sh"]

# Since in the classic UCS the ports 7636 and 7389 were only needed
# for avoiding conflict with Samba domain controller service
# they are not needed in this image
EXPOSE 389 636

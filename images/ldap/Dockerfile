###############################################################################
# Builder image for collecting Univention LDAP schema templates, base LDIFs
# and certain libraries that are maintained by Univention for UCS
# like cy2-saml
###############################################################################
ARG DOCKERHUB_CACHE
ARG DEBIAN_BASE_IMAGE_TAG
ARG DEB_BUILDER_REGISTRY
ARG DEB_BUILDER_IMAGE
ARG DEB_BUILDER_TAG
FROM ${DOCKERHUB_CACHE}debian:${DEBIAN_BASE_IMAGE_TAG} as ucs_builder

COPY sources.list /etc/apt/sources.list

WORKDIR /home/deb_packages

RUN chown _apt . && \
    echo 'nameserver 192.168.0.97' > /etc/resolv.conf && \
    apt-get update && \
    # These packages are only partially needed, and their dependencies
    # can and should not be met in Phoenix
    apt-get download \
        univention-appcenter \
        univention-self-service-passwordreset-umc \
        univention-ldap-config \
        univention-ldap-server \
        univention-saml-schema \
        univention-ldap-overlay-memberof \
        univention-ldap-acl-master \
        univention-portal \
        cy2-saml && \
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
FROM ${DOCKERHUB_CACHE}debian:${DEBIAN_BASE_IMAGE_TAG}

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

RUN apt-get update && \
    # Install apt-utils otherwise we can't seem to
    # do non-interactive package configuration
    apt-get install --no-install-recommends -y apt-utils=1.8.* && \
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
        liblasso3=2.6.* \
        libglib2.0-0=2.* \
        # 30 Mb extra, only needed for ucr-light-filter
        # TODO: Remove when "Config-Adapter" sidecar is ready
        python3=3.7.* && \
    rm -rf /var/lib/apt/lists/* && \
    # This file is a depencecy of the slapd.conf templates
    mkdir -p /var/lib/univention-ldap/schema/id/ && \
    echo "1" >/var/lib/univention-ldap/schema/id/id

###############################################################################
# Copy LDAP config and libs from UCS builder image
###############################################################################
# slapd.conf templates:
COPY --from=ucs_builder /usr/share/univention-ldap/schema \
                        /usr/share/univention-ldap/schema
COPY --from=ucs_builder /usr/lib/univention-portal/schema \
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
     /var/lib/univention-ldap/local-schema/univention-app.schema

COPY --from=ucs_builder \
     /usr/share/univention-self-service/self-service-passwordreset.schema \
     /var/lib/univention-ldap/local-schema/self-service-passwordreset.schema

COPY --from=ucs_builder \
     /usr/lib/univention-portal/schema/univention-portal.schema \
     /var/lib/univention-ldap/local-schema/univention-portal.schema

# ACLs:
COPY --from=ucs_builder \
     /usr/share/univention-appcenter/66univention-appcenter_app.acl \
     /etc/univention/templates/files/etc/ldap/slapd.conf.d/

COPY --from=ucs_builder \
     /usr/lib/univention-portal/acl/62univention-portal.acl \
     /etc/univention/templates/files/etc/ldap/slapd.conf.d/

# UCS only libraries:
COPY --from=ucs_builder \
     /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
     /usr/lib/x86_64-linux-gnu/sasl2/

###############################################################################
# Copy from OpenLDAP binary builder image
###############################################################################
COPY --from=deb_builder /root/src/debian/slapd_2.4.*_amd64.deb \
                        /tmp/

COPY --from=deb_builder /root/src/debian/libldap-2.4-2_2.4.*_amd64.deb \
                        /tmp/

RUN ln -s /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
          /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0 && \

    ln -s /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so.0.2.0 \
          /usr/lib/x86_64-linux-gnu/sasl2/libsaml.so && \

    apt-get install --assume-yes --no-install-recommends \
        /tmp/slapd_*.deb /tmp/libldap-*.deb

###############################################################################
# Copy from Docker build context
###############################################################################
COPY ucr /usr/sbin/
COPY ucr-light-filter /usr/sbin/

COPY container-entrypoint.sh /usr/local/bin

ENTRYPOINT ["container-entrypoint.sh"]

# Since in the classic UCS the ports 7636 and 7389 were only needed
# for avoiding conflict with Samba domain controller service
# they are not needed in this image
EXPOSE 389 636

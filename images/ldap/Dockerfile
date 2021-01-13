###############################################################################
# Builder image for collecting Univention LDAP schema templates and base LDIFs
###############################################################################
ARG DEBIAN_BASE_IMAGE_TAG
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
FROM debian:${DEBIAN_BASE_IMAGE_TAG} as deb_builder

RUN echo 'deb-src http://deb.debian.org/debian buster main' \
      >> /etc/apt/sources.list && \
    apt update && \
    apt install -y devscripts
 #&&
#    apt-get source --download-only  libldap-2.4-2
#
# apt-get build-dep doesn't get these two slapd dependencies:
# libgcrypt-dev libssl-dev
# Because these dependencies are added by Univention patches
# so apt-get build-dep has no chance of knowing about them.
# apt-utils is installed to avoid some warnings by build-dep
RUN mkdir -p ~/src/debian/ && cd ~/src/debian && chown _apt . && \
    apt-get install --assume-yes --no-install-recommends \
                    apt-utils libgcrypt-dev libssl-dev && \
    apt-get build-dep --assume-yes libldap-2.4-2 && \
    apt-get source libldap-2.4-2 && \
    cd openldap-2.4.47+dfsg && \
# Disabling dh_auto_test is need here as the patch for that is apparently broken
    sed -i 's/\tdh_auto_test/\t# dh_auto_test/' debian/rules

COPY patches/2.4.47+dfsg-3+deb10u4/ /tmp/2.4.47+dfsg-3+deb10u4/


# This is explicitly not wanted
#     patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/70_ppolicy_udm_lock.patch
# This is also explicitly not wanted as this causes debian dependency on univention-config
#    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/35_commit_slapd_init_script.patch && \
# This one doesn't seem to be relevant considering that in a container we won't use init scripts anyway
#     patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/80_slapd_init_start.patch
#
#
# I am pretty sure in a container image, after installation the process will be stopped...
#     patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/86_postinst_slapd_stop.patch
#
# We don't need to restart in postinstall during docker build.
# patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/87_postinst_slapd_restart.patch
#
# The "not yet understood reasons" that are mentioned in this patch
# doesn't seem to happen during docker build
# patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/93-exclude-ldap-utils-from-shlibs.patch
#
# 99_ITS-9370-check-for-equality-rule-on-old_rdn.quilt
# and
# 99_ITS-9384-remove-assert-in-obsolete-csnNormalize23.quilt
# seems to be the same as what is already in debian as
# debian/patches/ITS-9370-check-for-equality-rule-on-old_rdn.patch
# and
# debian/patches/ITS-9384-remove-assert-in-obsolete-csnNormalize23.patch
# and causing errors if applied twice
#
# 70_ppolicy_udm_lock.quilt is unwanted and depends on python2.7/Python.h
# what we really shouldn't do in 2021
# 99_Bug37915_avoid_deadlock_and_race_condition.quilt
# is essentailly a patch of the above patch so that is not needed either
# and doesn't work without the previous
RUN cd ~/src/debian/openldap-2.4.47+dfsg/ && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/03_dbgsym-migration.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/10_translog_overlay.patch && \
    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/12_k5pwd.patch && \
    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/15_pwd_scheme_kinit.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/20_core_schema.patch && \
    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/23_cosine_schema.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/30_postinst.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/53_dellog-2.3.30.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/55_libgcrypt.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/60_ssl.patch && \
    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/62_disable_tests.patch && \
    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/63_disable_migrate_to_slapd_d_style.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/85_disable_move_and_dump.patch && \
    patch -p0 < /tmp/2.4.47+dfsg-3+deb10u4/97_shadowbind_overlay_rules.patch && \
    patch -p1 < /tmp/2.4.47+dfsg-3+deb10u4/98_database_upgrade_version.patch && \
    rm /tmp/2.4.47+dfsg-3+deb10u4/70_ppolicy_udm_lock.quilt && \
    rm /tmp/2.4.47+dfsg-3+deb10u4/99_Bug37915_avoid_deadlock_and_race_condition.quilt && \
    rm /tmp/2.4.47+dfsg-3+deb10u4/99_ITS-9370-check-for-equality-rule-on-old_rdn.quilt && \
    rm /tmp/2.4.47+dfsg-3+deb10u4/99_ITS-9384-remove-assert-in-obsolete-csnNormalize23.quilt && \
    cp /tmp/2.4.47+dfsg-3+deb10u4/*.quilt debian/patches/ && \
    ls /tmp/2.4.47+dfsg-3+deb10u4/*.quilt | tr ' ' '\n' |cut -d '/' -f 4 >>  debian/patches/series && \
    dpkg-buildpackage -uc -us -b
    # fakeroot debian/rules binary

RUN ls -lah ~/src/debian/slapd*.deb

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

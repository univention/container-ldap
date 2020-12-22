FROM debian:buster-slim as builder

COPY sources.list /etc/apt/sources.list

RUN cd "$(mktemp --directory)" && chown _apt . && \
    apt-get update && \
    apt-get download \
                    slapd \
                    libldap-2.4-2  \
                    univention-ldap-config \
                    univention-ldap-server \
                    univention-saml-schema \
                    univention-virtual-machine-manager-schema \
                    univention-ldap-overlay-memberof \
                    univention-ldap-acl-master && \
    (dpkg --force-all -i ./*.deb || true)

###############################################################################
FROM debian:buster-slim

RUN apt-get update && \
    # Install apt-utils otherwise we can't seem to
    # do non-interactive package configuration
    apt-get install -y apt-utils && \
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
    apt-get install -y slapd \
                       libsasl2-2 \
                       libsasl2-modules \
                       libsasl2-modules-db \
                       libsasl2-modules-gssapi-heimdal \
                       krb5-config \
                       libgssapi-krb5-2 \
                       libkrb5-26-heimdal \
                       libkadm5srv8-heimdal \
                       openssl \
                       # 30 Mb extra, only needed for slapd.conf and ldif generation
                       # TODO: Remove when "Config-Adapter" sidecar is ready
                       python3

# As seen in /usr/share/univention-ldap/create-dh-parameter-files
RUN cd /etc/ldap && \
    openssl dhparam -out "dh_2048.pem" -2 2048 && \
    chmod 644 "dh_2048.pem" && \
    cd -

COPY --from=builder /etc/ldap/schema/core.schema /etc/ldap/schema/core.schema
COPY --from=builder /etc/ldap/schema/cosine.schema /etc/ldap/schema/cosine.schema
COPY --from=builder /etc/ldap/schema/nis.schema /etc/ldap/schema/nis.schema
COPY --from=builder /etc/univention/templates/files/etc/ldap/slapd.conf.d \
                    /etc/univention/templates/files/etc/ldap/slapd.conf.d
# This "info" file is also a dependency of the templates
COPY --from=builder /etc/univention/templates/info/univention-ldap-server.info \
                    /etc/univention/templates/info/univention-ldap-server.info
COPY --from=builder /usr/lib/ldap/translog.so /usr/lib/ldap/translog.so
COPY --from=builder /usr/lib/ldap/k5pwd.so /usr/lib/ldap/k5pwd.so
COPY --from=builder /usr/lib/ldap/pwd_scheme_kinit.so /usr/lib/ldap/pwd_scheme_kinit.so
COPY --from=builder /usr/lib/ldap/shadowbind.so /usr/lib/ldap/shadowbind.so
COPY --from=builder /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.10 \
                    /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.10
COPY --from=builder /usr/share/univention-ldap/schema /usr/share/univention-ldap/schema
COPY --from=builder /usr/share/univention-ldap/base.ldif /usr/share/univention-ldap/base.ldif
COPY --from=builder /usr/share/univention-ldap/core-edition.ldif /usr/share/univention-ldap/core-edition.ldif
COPY --from=builder /usr/share/univention-ldap/translog.ldif /usr/share/univention-ldap/translog.ldif
COPY --from=builder /var/lib/univention-ldap/ /var/lib/univention-ldap/

COPY                local-schema /var/lib/univention-ldap/local-schema
COPY                ucr /usr/sbin/
COPY                solve.py /usr/sbin/
COPY                Administrator_user.ldif /Administrator_user.ldif

COPY                container-entrypoint.sh /usr/local/bin

ENTRYPOINT ["container-entrypoint.sh"]

# Since in the classic UCS the ports 7636 and 7389 were only needed
# for avoiding conflict with Samba domain controller service
# they are not needed in this image
EXPOSE 389 636

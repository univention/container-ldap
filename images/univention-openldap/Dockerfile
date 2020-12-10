ARG SUITE
FROM debian:${SUITE}



RUN useradd Administrator \
    -p $6$6M7LMsXo2wgniZGE$tGxma/MBb1kUqx9.GZ8UwpvEwOXUXalcyYOykGebUU2EBdccOPCWDyKmvIOsDjDw1vVRb7TW9V4vxxtjB6Yqw.

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
                       openssl

COPY etc/ldap/dh_2048.pem /etc/ldap/dh_2048.pem
COPY etc/ldap/slapd.conf /etc/ldap/slapd.conf
COPY etc/ldap/schema/core.schema /etc/ldap/schema/core.schema
COPY etc/ldap/schema/cosine.schema /etc/ldap/schema/cosine.schema
COPY etc/ldap/schema/nis.schema /etc/ldap/schema/nis.schema
COPY etc/univention/ssl /etc/univention/ssl
COPY usr/lib/ldap/translog.so /usr/lib/ldap/translog.so
COPY usr/lib/ldap/k5pwd.so /usr/lib/ldap/k5pwd.so
COPY usr/lib/ldap/pwd_scheme_kinit.so /usr/lib/ldap/pwd_scheme_kinit.so
COPY usr/lib/ldap/shadowbind.so /usr/lib/ldap/shadowbind.so
COPY usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.10 /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2.10.10
COPY usr/share/univention-ldap/ /usr/share/univention-ldap/
COPY var/lib/univention-ldap/ /var/lib/univention-ldap/

ENTRYPOINT ["/usr/sbin/slapd", "-f", "/etc/ldap/slapd.conf", "-d", "9999", "-h", "ldapi:/// ldap://:389/ ldaps://:636/"]

# Since in the classic UCS the ports 7636 and 7389 were only needed
# for avoiding conflict with Samba domain controller service
# they are not needed in this image
EXPOSE 389 636

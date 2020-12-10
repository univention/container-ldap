#!/usr/bin/env bash
SUITES=(stretch buster bullseye)
SUITE=${SUITES[1]}

OMAR_UCS_5="/var/univention/buildsystem2/apt/ucs_5.0-0/"
UNIV_PATCHED_SLAPD_DEB="amd64/slapd_2.4.47+dfsg-3+deb10u2A~5.0.0.202008031848_amd64.deb"
UNIV_PATCHED_LLDAP_DEB="amd64/libldap-2.4-2_2.4.47+dfsg-3+deb10u2A~5.0.0.202008031848_amd64.deb"
#UNIV_LDAP_SRV="all/univention-ldap-server_16.0.4-2A~5.0.0.202011301749_all.deb"
#UNIV_NOTIFIER="amd64/univention-directory-notifier_14.0.4-3A~5.0.0.202012011441_amd64.deb"
if [[ ! -f "${UNIV_PATCHED_SLAPD_DEB##*/}" ]];
then
    scp "omar:${OMAR_UCS_5}/${UNIV_PATCHED_SLAPD_DEB}" .
    scp "omar:${OMAR_UCS_5}/${UNIV_PATCHED_LLDAP_DEB}" .
    #scp "omar:${OMAR_UCS_5}/${UNIV_LDAP_SRV}" .
    #scp "omar:${OMAR_UCS_5}/${UNIV_NOTIFIER}" .
    ar vx "${UNIV_PATCHED_SLAPD_DEB##*/}" data.tar.xz
    tar -xf data.tar.xz -C univention-openldap/
    ar vx "${UNIV_PATCHED_LLDAP_DEB##*/}" data.tar.xz
    tar -xf data.tar.xz -C univention-openldap/

    # TODO: Use /usr/share/univention-ssl/make-certificates.sh
    scp galant:~fgeczi/ssl_fg-organization.tar.bz2 .
    tar -xf ssl_fg-organization.tar.bz2 -C univention-openldap/

    # TODO: Extract schemas from NOTIFIER and LDAP_SRV
    scp galant:~fgeczi/univention-ldap_schemas.tar.bz2 .
    tar -xf univention-ldap_schemas.tar.bz2 -C univention-openldap/

    # TODO: Eliminate this as soon as it can be generated
    cp slapd.conf_current univention-openldap/etc/ldap/slapd.conf

    # As seen in /usr/share/univention-ldap/create-dh-parameter-files
    openssl dhparam -out "dh_2048.pem" -2 2048
    chmod 644 "dh_2048.pem"
    mv "dh_2048.pem" "univention-openldap/etc/ldap/"

fi

docker build -t univention-openldap:${SUITE}-slim-portable \
             --build-arg SUITE=${SUITE}-slim \
             -f ./univention-openldap/Dockerfile ./univention-openldap

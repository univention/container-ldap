#!/usr/bin/env bash
SUITES=(stretch buster bullseye)
SUITE=${SUITES[1]}

OMAR_UCS_5="/var/univention/buildsystem2/apt/ucs_5.0-0/"
UNIV_PATCHED_SLAPD_DEB="amd64/slapd_2.4.47+dfsg-3+deb10u2A~5.0.0.202008031848_amd64.deb"
UNIV_PATCHED_LLDAP_DEB="amd64/libldap-2.4-2_2.4.47+dfsg-3+deb10u2A~5.0.0.202008031848_amd64.deb"
UNIV_LDAP_CFG="all/univention-ldap-config_16.0.4-2A~5.0.0.202011301749_all.deb"
UNIV_LDAP_SRV="all/univention-ldap-server_16.0.4-2A~5.0.0.202011301749_all.deb"
UNIV_SAML_SCH="all/univention-saml-schema_7.0.4-2A~5.0.0.202012081116_all.deb"
UNIV_VIRT_SCH="all/univention-virtual-machine-manager-schema_10.0.0-1A~5.0.0.202006052312_all.deb"
UNIV_MMBR_SCH="all/univention-ldap-overlay-memberof_12.0.0-1A~5.0.0.202009231618_all.deb"
UNIV_ACLM_SCH="all/univention-ldap-acl-master_16.0.4-2A~5.0.0.202011301749_all.deb"
UNIV_APPC_SCH="all/univention-appcenter_9.0.1-7A~5.0.0.202012141225_all.deb"

#UNIV_NOTIFIER="amd64/univention-directory-notifier_14.0.4-3A~5.0.0.202012011441_amd64.deb"
if [[ ! -f "${UNIV_PATCHED_SLAPD_DEB##*/}" ]];
then
    scp "omar:${OMAR_UCS_5}/${UNIV_PATCHED_SLAPD_DEB}" .
    scp "omar:${OMAR_UCS_5}/${UNIV_PATCHED_LLDAP_DEB}" .
    scp "omar:${OMAR_UCS_5}/${UNIV_LDAP_SRV}" .
    scp "omar:${OMAR_UCS_5}/${UNIV_SAML_SCH}" .

    #scp "omar:${OMAR_UCS_5}/${UNIV_NOTIFIER}" .
    ar vx "${UNIV_PATCHED_SLAPD_DEB##*/}" data.tar.xz
    tar -xf data.tar.xz -C univention-openldap/
    ar vx "${UNIV_PATCHED_LLDAP_DEB##*/}" data.tar.xz
    tar -xf data.tar.xz -C univention-openldap/
    ar vx "${UNIV_LDAP_SRV##*/}" data.tar.xz
    tar -xf data.tar.xz -C univention-openldap/

    ar vx "${UNIV_LDAP_CFG##*/}" data.tar.xz
    tar -C univention-openldap/ -xf data.tar.xz ./usr/share/univention-ldap/base.ldif \
                                                ./usr/share/univention-ldap/core-edition.ldif \
                                                ./usr/share/univention-ldap/translog.ldif \
                                                ./usr/share/univention-ldap/ffpu.ldif

    ar vx "${UNIV_SAML_SCH##*/}" data.tar.xz
    tar -C univention-openldap/ -xf data.tar.xz ./etc/univention/templates/files/etc/ldap/slapd.conf.d/

    ar vx "${UNIV_VIRT_SCH##*/}" data.tar.xz
    tar -C univention-openldap/ -xf data.tar.xz ./etc/univention/templates/files/etc/ldap/slapd.conf.d/

    ar vx "${UNIV_MMBR_SCH##*/}" data.tar.xz
    # TODO: Do we need the univention-update-memberof python tool?
    tar -C univention-openldap/ -xf data.tar.xz ./etc/univention/templates/files/etc/ldap/slapd.conf.d/

    ar vx "${UNIV_ACLM_SCH##*/}" data.tar.xz
    tar -C univention-openldap/ -xf data.tar.xz ./etc/univention/templates/files/etc/ldap/slapd.conf.d/

    ar vx "${UNIV_APPC_SCH##*/}" data.tar.xz
    tar -C univention-openldap/ -xf data.tar.xz ./usr/share/univention-appcenter/66univention-appcenter_app.acl
    mv univention-openldap/usr/share/univention-appcenter/66univention-appcenter_app.acl \
       univention-openldap/etc/univention/templates/files/etc/ldap/slapd.conf.d/

    # TODO: Use /usr/share/univention-ssl/make-certificates.sh
    scp galant:~fgeczi/ssl_fg-organization.tar.bz2 .
    tar -xf ssl_fg-organization.tar.bz2 -C univention-openldap/

    # TODO: Extract schemas from NOTIFIER and LDAP_SRV
    scp galant:~fgeczi/univention-ldap_schemas.tar.bz2 .
    tar -xf univention-ldap_schemas.tar.bz2 -C univention-openldap/

    # As seen in /usr/share/univention-ldap/create-dh-parameter-files
    openssl dhparam -out "dh_2048.pem" -2 2048
    chmod 644 "dh_2048.pem"
    mv "dh_2048.pem" "univention-openldap/etc/ldap/"

    # TODO: Find a way to have the translog overlay do this
    mkdir -p univention-openldap/var/lib/univention-ldap/listener/
    touch univention-openldap/var/lib/univention-ldap/listener/listener

    cp ucr solve.py univention-openldap/usr/sbin/
fi

docker build -t univention-openldap:${SUITE}-slim-portable \
             --build-arg SUITE=${SUITE}-slim \
             -f ./univention-openldap/Dockerfile ./univention-openldap

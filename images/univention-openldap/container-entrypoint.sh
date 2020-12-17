#!/usr/bin/env bash

set -x

setup_slapd_conf() {

    cat /etc/univention/templates/files/etc/ldap/slapd.conf.d/* |\
    solve.py --ldapbase 'dc=fg-organization,dc=intranet' \
             --domainname 'fg-organization.intranet' \
             > /etc/ldap/slapd.conf
}

setup_initial_ldif() {
    # Inspired by 01univention-ldap-server-init.inst
    pw_crypt="univention"
    backup_crypt="univention"
    ldap_base="dc=fg-organization,dc=intranet"
    domainname="fg-organization.intranet"
    sambadomain="${domainname%%.*}"
    realm="$(echo "$domainname" | sed -e 's/dc=//g;s/,/./g;s/[a-z]/\u&/g')"
    firstdc="$(echo "$ldap_base" | sed -e 's|,.*||g;s|.*=||')"

    # TODO: use check /usr/sbin/univention-newsid
    sid="S-1-5-21-4181270633-4020214626-836608356"

    printf -v filter_string '%s' \
         "s|@@%%@@ldap\.pw@@%%@@|$pw_crypt|;"\
         "s|@@%%@@backup\.pw@@%%@@|$backup_crypt|;"\
         "s|@@%%@@sambadomain@@%%@@|$sambadomain|;"\
         "s|@@%@@sambadomain@@%@@|$sambadomain|;"\
         "s|@@%%@@firstdc@@%%@@|$firstdc|;"\
         "s|@@%%@@realm@@%%@@|$realm|;"\
         "s|@@%%@@sid@@%%@@|$sid|;"\
         "s|@@%@@domain@@%@@|$domainname|"

    cat /usr/share/univention-ldap/base.ldif \
        /usr/share/univention-ldap/core-edition.ldif |\
    solve.py --ldapbase "${ldap_base}" --domainname "${domainname}"|\
    sed -e "${filter_string}" | slapadd -f /etc/ldap/slapd.conf 
}

setup_translog_ldif() {
    # Inspired by /usr/share/univention-ldap/setup-translog
    slapadd -f /etc/ldap/slapd.conf -b cn=translog \
            -l /usr/share/univention-ldap/translog.ldif
}

setup_listener_path() {
    # TODO: Shouldn't the translog overlay be able to do this?
    mkdir -p /var/lib/univention-ldap/listener/
    touch /var/lib/univention-ldap/listener/listener
}


setup_slapd_conf
setup_initial_ldif
setup_translog_ldif
setup_listener_path

# TODO: Remove this
sed -i '/^rootdn\t\t.*/a rootpw\t\t"univention"' /etc/ldap/slapd.conf

/usr/sbin/slapd -f /etc/ldap/slapd.conf -d 9999 -h "ldapi:/// ldap://:389/ ldaps://:636/"

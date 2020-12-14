#!/usr/bin/env bash



# As seen in 01 univention-ldap-server-init.inst
pw_crypt="0123_pwd_crypt"
backup_crypt="0123backup_crypt"
sambadomain="0123sambadomain"
firstdc="0123firstdc"
realm="0123realm"
sid="0123sid"
Domain="fg-organization.intranet"

LDAP_BASE="dc=fg-organization,dc=intranet"


#cat /usr/share/univention-ldap/base.ldif /usr/share/univention-ldap/core-edition.ldif |
cat ./univention-ldap/base.ldif ./univention-ldap/core-edition.ldif | ./solve.py --ldapbase "${LDAP_BASE}" --domainname "${Domain}" |\
     sed -e \
    "s|@@%%@@ldap\.pw@@%%@@|$pw_crypt|;s|@@%%@@backup\.pw@@%%@@|$backup_crypt|;s|@@%%@@sambadomain@@%%@@|$sambadomain|;s|@@%%@@firstdc@@%%@@|$firstdc|;s|@@%%@@realm@@%%@@|$realm|;s|@@%%@@sid@@%%@@|$sid|;s|@@%@@domain@@%@@|$Domain|"


#slapadd -f /etc/ldap/slapd.conf >>/var/log/univention/join.log 2>&1 ||

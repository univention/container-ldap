#!/usr/bin/env bash

touch /var/lib/univention-ldap/listener/listener

cat /etc/univention/templates/files/etc/ldap/slapd.conf.d/* | solve.py --ldapbase 'dc=fg-organization,dc=intranet' --domainname 'fg-organization.intranet' > /etc/ldap/slapd.conf

# TODO: Remove this
sed -i '/^rootdn\t\t.*/a rootpw\t\t"univention"' /etc/ldap/slapd.conf



/usr/sbin/slapd -f /etc/ldap/slapd.conf -d 9999 -h "ldapi:/// ldap://:389/ ldaps://:636/"

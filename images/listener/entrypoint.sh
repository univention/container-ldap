#!/bin/bash
set -euxo pipefail

cat <<EOF > /etc/ldap/ldap.conf
# This file should be world readable but not world writable.

TLS_CACERT /etc/univention/ssl/ucsCA/CAcert.pem

URI ${LDAP_URI}

BASE	${LDAP_BASE_DN}
EOF

echo "${LDAP_BIND_PASSWORD}" > /etc/ldap.secret

exec "/usr/sbin/univention-directory-listener" "$@"

# [EOF]

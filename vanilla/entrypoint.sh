#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

set -euo pipefail

DATA_DIR="/var/lib/ldap"

# Read admin password from Docker secret or env var
if [ -f /run/secrets/ldap_admin_pw ]; then
  LDAP_ADMIN_PW="$(cat /run/secrets/ldap_admin_pw)"
fi
: "${LDAP_ADMIN_PW:?Set LDAP_ADMIN_PW or mount a Docker secret at /run/secrets/ldap_admin_pw}"

# Verify writable directories
for dir in "${DATA_DIR}" /etc/ldap; do
  if [ ! -w "${dir}" ]; then
    echo "ERROR: ${dir} is not writable. Ensure it is owned by uid 100 (openldap)." >&2
    exit 1
  fi
done

# Write hashed rootpw to a separate file included by slapd.conf
echo "rootpw $(slappasswd -s "${LDAP_ADMIN_PW}")" > /etc/ldap/rootpw.conf

# Load seed data, skipping entries that already exist (-c)
if [ -f /seed/seed.ldif ]; then
  slapadd -c -f /etc/ldap/slapd.conf -l /seed/seed.ldif || true
fi

echo "Starting slapd..."
exec /usr/sbin/slapd \
  -f /etc/ldap/slapd.conf \
  -d "${LDAP_LOG_LEVEL:-stats}" \
  -h "ldap://:389/"

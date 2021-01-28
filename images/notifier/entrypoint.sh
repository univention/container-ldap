#!/bin/bash
set -euxo pipefail

if [[ ! -d "/var/lib/univention-ldap/listener/" ]]; then
  echo "The listener dir is missing!"
  echo "It should be a shared volume with the OpenLDAP container."
  exit 2
fi

if [[ ! -d "/var/run/slapd/" ]]; then
  echo "The slapd run dir is missing!"
  echo "It should be a shared volume with the OpenLDAP container."
  exit 3
fi

# The notifier writes an error message to its log-file if this file is missing.
# Because it lives in a volume, it can not be created during build.
touch /var/lib/univention-ldap/notify/transaction
touch /var/lib/univention-ldap/notify/transaction.lock

mkdir /var/log/univention/

if [[ ! -e "/var/lib/univention-ldap/listener/listener" ]]; then
  echo "The listener file is missing!"
  echo "It should get created by the slapd translog overlay-module."
  exit 1
fi

transaction_path='/var/lib/univention-ldap/notify/transaction'
if [[ -s "${transaction_path}" ]]; then
  echo "Found pending transactions"
  last_id="$(awk 'END{print $1}' "${transaction_path}")"
  echo "Last transaction: ${last_id}"
  translog_result=$(/usr/share/univention-directory-notifier/univention-translog ldap "$last_id" >/dev/null)
  if [[ "${translog_result}" -gt "1" ]]; then
    echo "Bad translog result: ${translog_result}"
    exit 2
  elif [[ "${translog_result}" -eq "1" ]]; then
    echo "Importing from translog to LDAP"
    /usr/share/univention-directory-notifier/univention-translog --lenient import
  fi
fi

echo "Starting notifier daemon"
exec "/usr/sbin/univention-directory-notifier" "$@"

# [EOF]

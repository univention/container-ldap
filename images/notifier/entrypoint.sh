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

# Both notifier and slapd need to be able to write this lock-file.
# The slapd writes to it on db-change, not on startup.
# The notifier writes to it whenever data is found in the "listener"-file.
touch /var/lib/univention-ldap/listener/listener.lock

# Wait for the openldap container to create ldapi and translog file
echo "Waiting for the listener and ldapi files:"
waited_seconds=0
while [[ ! -e "/var/lib/univention-ldap/listener/listener" ]] &&
    [[ ! -e "/var/run/slapd/ldapi" ]]; do
  if [[ waited_seconds -gt 10 ]]; then
    echo "Waited for too long"
    exit 4
  fi
  echo -n "."
  sleep 1
  (( waited_seconds++ )) || true
done
echo "Found the needed files after ${waited_seconds} seconds"

# Check for pending transations
transaction_path='/var/lib/univention-ldap/notify/transaction'
if [[ -s "${transaction_path}" ]]; then
  echo "Found pending transactions"
  last_id="$(awk 'END{print $1}' "${transaction_path}")"
  echo "Last transaction: ${last_id}"
  translog_result=$(/usr/share/univention-directory-notifier/univention-translog ldap "$last_id" >/dev/null)
  if [[ "${translog_result}" -gt "1" ]]; then
    echo "Bad translog result: ${translog_result}"
    exit 5
  elif [[ "${translog_result}" -eq "1" ]]; then
    echo "Importing from translog to LDAP"
    /usr/share/univention-directory-notifier/univention-translog --lenient import
  fi
fi

EXIT_CODE=0
echo "Starting notifier daemon"
"/usr/sbin/univention-directory-notifier" "$@" || EXIT_CODE=$?

echo "Notifier exited with ${EXIT_CODE}"
cat /var/log/univention/notifier.log

exit ${EXIT_CODE}

# [EOF]

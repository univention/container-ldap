#!/bin/bash
set -euxo pipefail
shopt -s expand_aliases

alias tsecho='echo "$(date --utc +%Y-%m-%dT%H:%M:%SZ)"'

EXIT_CODE=0
tsecho "Starting notifier daemon"
/usr/sbin/univention-directory-notifier "$@" || EXIT_CODE=$?

tsecho "Notifier exited with ${EXIT_CODE}"

exit ${EXIT_CODE}

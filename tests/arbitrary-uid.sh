#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH
#
# Run a container image like OpenShift's SecurityContextConstraint "restricted-v2" does:
# with an arbitrary user ID that is not in /etc/passwd and the group ID 0. Fail if files
# of the image can't be read, directories can't be traversed or the given directories
# aren't writable. The check runs inside the image, so it sees the real permissions.
#
#   tests/arbitrary-uid.sh IMAGE [--ignore PATH]... [--writable PATH]... [--run COMMAND]
#
#   --ignore PATH    skip a path the image doesn't use at runtime
#   --writable PATH  directory that must be writable
#   --run COMMAND    shell command that must succeed as the arbitrary user
set -eu

image=$1
shift
# Root-only on every Debian system, irrelevant for the services; build leftovers in /tmp
prune="/proc /sys /dev /tmp /root /var/log /var/lib/dpkg /var/lib/apt/lists /var/cache/apt
  /var/cache/debconf /var/cache/ldconfig /var/spool/cron /etc/ssl/private /usr/lib/ssl/private
  /etc/shadow /etc/shadow- /etc/gshadow /etc/gshadow- /etc/passwd- /etc/group- /etc/.pwd.lock
  /etc/at.deny /etc/security/opasswd /etc/sudoers /etc/sudoers.d"
writable=""
run="true"
while [ $# -gt 0 ]; do
  case $1 in
    --ignore) prune="$prune $2" ;;
    --writable) writable="$writable $2" ;;
    --run) run=$2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift 2
done

expr=""
for path in $prune; do
  expr="$expr -path $path -o"
done

# Symlinks are skipped: their targets are checked themselves, dangling links don't matter.
check="
problems=\$(find / -xdev \\( $expr -false \\) -prune -o ! -type l \\( ! -readable -o -type d ! -executable \\) -print 2>/dev/null)
[ -z \"\$problems\" ] || { echo 'not readable for UID '\$(id -u)' GID '\$(id -g)':'; echo \"\$problems\" | sed 's/^/  /'; exit 1; }
for dir in $writable; do
  [ -w \"\$dir\" ] || { echo \"not writable: \$dir\"; exit 1; }
done
$run || { echo 'failed: $run'; exit 1; }
echo 'OK: usable with UID '\$(id -u)' and GID '\$(id -g)
"

docker run --rm --user 1000760000:0 --entrypoint /bin/sh "$image" -c "$check"

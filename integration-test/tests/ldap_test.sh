#!/usr/bin/env bash

export LDAP_CONTAINER="container-ldap_openldap_1"
export LDAP_BASE_DN="dc=univention-organization,dc=intranet"


translog_overlay () {
  translog_exists="$(\
    ldapsearch -x -h "${LDAP_CONTAINER}" -p 389 \
               -D "cn=admin,${LDAP_BASE_DN}" \
               -w univention -b cn=translog \
    || true)"

  if [[ -n "${translog_exists}" ]]; then
    echo "TEST OK: Translog overlay can be found with cn=admin"
    #echo "${translog_exists}"
    return 0
  fi

  echo "ERROR: Translog overlay doesn't exist!">&2
  echo "${translog_exists}">&2
  exit 1
}

## bugs: [39878, 34203]
anonymous_search () {
  insufficient_access="$(
  LC_ALL=C \
  ldapsearch -LLLo ldif-wrap=no \
             -H "ldap://${LDAP_CONTAINER}:389" \
             -x -b "${LDAP_BASE_DN}" \
             -s base '(objectClass=*)' dn 2>&1 \
  && true)"

  if [[ 'Insufficient access (50)' == "${insufficient_access}" ]]; then
    echo "TEST OK: Anonymous user has insufficient access"
    return 0
  fi

  echo "ERROR: Anonymous read should not be allowed!">&2
  echo "${insufficient_access}">&2
  exit 1
}

cn_backup_user () {
  backup_user_exists="$(\
    ldapsearch -x -h "${LDAP_CONTAINER}" -p 389 \
               -D "cn=backup,${LDAP_BASE_DN}" \
               -w univention123 -b "cn=backup,${LDAP_BASE_DN}" \
    || true)"

  if [[ -n "${backup_user_exists}" ]]; then
    echo "TEST OK: Backup cn=backup user can query itself"
    #echo "${backup_user_exists}"
    return 0
  fi

  echo "ERROR: Backup user doesn't exist!">&2
  echo "${backup_user_exists}">&2
  exit 1
}

translog_overlay
anonymous_search
cn_backup_user

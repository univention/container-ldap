#!/usr/bin/env bash

set -euxo pipefail

init_variables() {
  DOMAIN_NAME="${DOMAIN_NAME:-fg-organization.intranet}"
  LDAP_BASE_DN="${LDAP_BASE_DN:-dc=fg-organization,dc=intranet}"
}

setup_listener_path() {
  # TODO: Shouldn't the translog overlay be able to do this?
  mkdir --parents /var/lib/univention-ldap/listener/
  touch /var/lib/univention-ldap/listener/listener
}

setup_last_id_path() {
  # Docker persistent named volumes can only be mapped to directories
  # and since certain directories under /var/lib/univention-ldap/
  # have to be taken from the image we can't map a volume to
  # /var/lib/univention-ldap/ directly.
  # The last_id path is hardcoded in translog overlay and can't be changed.
  # So in order to keep the last_id file on a separate volum
  # we mount a volume under /var/lib/univention-ldap/last-id-data/
  # and create a symbolic link in runtime.
  if [[ ! -L /var/lib/univention-ldap/last_id ]]; then
    mkdir --parents /var/lib/univention-ldap/last-id-data/
    touch /var/lib/univention-ldap/last-id-data/last_id
    ln --symbolic /var/lib/univention-ldap/last-id-data/last_id \
                  /var/lib/univention-ldap/last_id
  fi

  # If the last_id file exists, then it should never be empty
  # otherwise the translog overlay gets stuck at ID -1
  if [[ ! -s /var/lib/univention-ldap/last_id ]]; then
    echo '0' > /var/lib/univention-ldap/last_id
  fi
}

setup_slapd_conf() {

  cat /etc/univention/templates/files/etc/ldap/slapd.conf.d/* \
    | solve.py --ldapbase "${LDAP_BASE_DN}" \
               --domainname "${DOMAIN_NAME}" \
               > /etc/ldap/slapd.conf
}

setup_initial_ldif() {
  # Inspired by 01univention-ldap-server-init.inst

  #if [[ "mdb" = "$ldap_database_type" ]; then
  if true; then # Let's assume that type is always mdb
    database_name="data"
  fi

  files="$(find /var/lib/univention-ldap/ldap/ -name "${database_name}.*" -type f)"

  if [[ ! -z "${files}" ]]; then
    return 0
  fi

  pw_crypt="univention"
  backup_crypt="univention"
  ldap_base="${LDAP_BASE_DN}"
  domainname="${DOMAIN_NAME}"
  sambadomain="${domainname%%.*}"
  realm="$(echo "$domainname" | sed -e 's/dc=//g;s/,/./g;s/[a-z]/\u&/g')"
  firstdc="$(echo "$ldap_base" | sed -e 's|,.*||g;s|.*=||')"

  # TODO: check /usr/sbin/univention-newsid
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
      /usr/share/univention-ldap/core-edition.ldif \
    | solve.py --ldapbase "${ldap_base}" --domainname "${domainname}" \
    | sed -e "${filter_string}" \
    | slapadd -f /etc/ldap/slapd.conf
}

setup_translog_ldif() {
  # Inspired by /usr/share/univention-ldap/setup-translog
  translog_exists="$(slapcat -f /etc/ldap/slapd.conf \
                             -b cn=translog \
                             -H 'ldap:///cn=translog??base' || true)"

  if [[ -n "${translog_exists}" ]]; then
    return 0
  fi

  slapadd -f /etc/ldap/slapd.conf \
          -b cn=translog \
          -l /usr/share/univention-ldap/translog.ldif
}

setup_administrator_user() {
  printf -v password_hash '%s' \
    '$6$6M7LMsXo2wgniZGE$tGxma/MBb1kUqx9.GZ8UwpvEwOXUXal' \
    'cyYOykGebUU2EBdccOPCWDyKmvIOsDjDw1vVRb7TW9V4vxxtjB6Yqw.'

  useradd Administrator --password "${password_hash}"


  admin_exists="$(slapcat -f /etc/ldap/slapd.conf \
                          -b uid=Administrator,cn=users,${LDAP_BASE_DN} \
                  || true)"

  if [[ -n "${admin_exists}" ]]; then
    return 0
  fi

  cat /Administrator_user.ldif \
    | solve.py --ldapbase "${LDAP_BASE_DN}" --domainname "${DOMAIN_NAME}" \
    | slapadd -f /etc/ldap/slapd.conf
}

setup_ssl_certificates() {
  # TODO: Fix this in Config Adapter
  # Check univention-ssl/debian/univention-ssl.postinst
  # and make-certificates.sh
  target_dir="/etc/univention/ssl/ucs-6045.${DOMAIN_NAME}"
  mkdir --parents "${target_dir}" /etc/univention/ssl/ucsCA/

  ln -s "${CA_CERT_FILE}" /etc/univention/ssl/ucsCA/CAcert.pem
  ln -s "${CERT_PEM_FILE}" "${target_dir}/cert.pem"
  ln -s "${PRIVATE_KEY_FILE}" "${target_dir}/private.key"

}


init_variables
setup_listener_path
setup_last_id_path
setup_slapd_conf
setup_initial_ldif
setup_translog_ldif
setup_administrator_user
setup_ssl_certificates

# TODO: Remove this
#sed -i '/^rootdn\t\t.*/a rootpw\t\t"univention"' /etc/ldap/slapd.conf

/usr/sbin/slapd -f /etc/ldap/slapd.conf \
                -d 9999 \
                -h "ldapi:/// ldap://:389/ ldaps://:636/"
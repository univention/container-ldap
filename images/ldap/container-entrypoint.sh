#!/usr/bin/env bash

set -euxo pipefail

check_unset_variables() {
  # Also list here the variables needed by ucr-light-filter
  var_names=( "DOMAIN_NAME" "LDAP_BASE_DN" \
              "LDAP_CN_ADMIN_PW_HASH" \
              "CA_CERT_FILE" "CERT_PEM_FILE" "PRIVATE_KEY_FILE" )
  for var_name in "${var_names[@]}"; do
    if [[ -z "${!var_name:-}" ]]; then
      echo "ERROR: '${var_name}' is unset."
      var_unset=true
    fi
  done

  if [[ -n "${var_unset:-}" ]]; then
    exit 1
  fi
}

setup_paths() {
  mkdir --parents /var/lib/univention-ldap/ldap
  mkdir --parents /var/lib/univention-ldap/translog
}

setup_symlinks() {
  # Some files from the local image are expected under
  # /var/lib/univention-ldap, using symlinks to make them available.
  if [ ! -L /var/lib/univention-ldap/local-schema ]
  then
    ln --symbolic /var/lib/univention-ldap-local/local-schema /var/lib/univention-ldap/
  fi
  if [ ! -L /var/lib/univention-ldap/schema ]
  then
    ln --symbolic /var/lib/univention-ldap-local/schema /var/lib/univention-ldap/
  fi
}

setup_listener_path() {
  # TODO: Shouldn't the translog overlay be able to do this?
  mkdir --parents /var/lib/univention-ldap/listener/
  touch /var/lib/univention-ldap/listener/listener
}

setup_last_id_path() {
  # If the last_id file exists, then it should never be empty
  # otherwise the translog overlay gets stuck at ID -1
  touch /var/lib/univention-ldap/last_id
  if [[ ! -s /var/lib/univention-ldap/last_id ]]; then
    echo "Setting 'last_id' to '0' because it is empty"
    echo -n '0' > /var/lib/univention-ldap/last_id
  fi
}

setup_slapd_conf() {
  cat /etc/univention/templates/files/etc/ldap/slapd.conf.d/* \
    | ucr-light-filter > /etc/ldap/slapd.conf
}

setup_sasl_mech_whitelist() {
  printf "%s\n" "mech_list: GSSAPI SAML EXTERNAL" \
    > /etc/ldap/sasl2/slapd.conf
}

setup_sasl_mech_saml() {
  if [[ -n "${SERVICE_PROVIDERS:-}" ]]; then
    # We have to modify the template since the hardcoded univention/saml/metadata
    # URL endpoint is not necessarily valid for future service providers.
    # Therefore we expect comma a separated list of URLs in SERVICE_PROVIDERS.
    # And since our Identitiy Providers are not UMC anymore but Keycloak or Gluu,
    # we put the metadata XMLs into a vendor neutral location.
    # The sp library is not quite usable nor desired in this context so that
    # and it's dependency sys are removed.

    printf -v filter_string '%s' \
     's/#@%@UCRWARNING=# @%@//;' \
     's/import sys/import os/;' \
     '/sys.path.insert/,+1d;' \
     's/univention-management-console//;' \
     '/service_providers =/,+3d;' \
     '/if identity_provider/i ' \
     'service_providers = os.environ["SERVICE_PROVIDERS"].split(",")'

    sed -e "${filter_string}" \
      /etc/univention/templates/files/etc/ldap/sasl2/slapd.conf \
      | ucr-light-filter >> /etc/ldap/sasl2/slapd.conf
  fi
}

setup_initial_ldif() {
  # Inspired by 01univention-ldap-server-init.inst

  #if [[ "mdb" = "$ldap_database_type" ]; then
  if true; then # Let's assume that type is always mdb
    database_name="data"
  fi

  files="$(find /var/lib/univention-ldap/ldap/ -name "${database_name}.*" -type f)"

  if [[ -n "${files}" ]]; then
    return 0
  fi

  pw_crypt="${LDAP_CN_ADMIN_PW_HASH}"
  ldap_base="${LDAP_BASE_DN}"
  domainname="${DOMAIN_NAME}"
  sambadomain="${domainname%%.*}"
  realm="$(echo "$domainname" | sed -e 's/dc=//g;s/,/./g;s/[a-z]/\u&/g')"
  firstdc="$(echo "$ldap_base" | sed -e 's|,.*||g;s|.*=||')"

  # TODO: check /usr/sbin/univention-newsid
  sid="S-1-5-21-UNSET"

  printf -v filter_string '%s' \
    "s|@@%%@@ldap\\.pw@@%%@@|$pw_crypt|;"\
    "s|@@%%@@sambadomain@@%%@@|$sambadomain|;"\
    "s|@@%@@sambadomain@@%@@|$sambadomain|;"\
    "s|@@%%@@firstdc@@%%@@|$firstdc|;"\
    "s|@@%%@@realm@@%%@@|$realm|;"\
    "s|@@%%@@sid@@%%@@|$sid|;"\
    "s|@@%@@domain@@%@@|$domainname|"

  # Remove cn=backup user as we don't need it
  sed -i '/cn=backup/,+6d' /usr/share/univention-ldap/base.ldif

  cat /usr/share/univention-ldap/{base.ldif,core-edition.ldif} \
    | ucr-light-filter | sed -e "${filter_string}" \
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

setup_ssl_certificates() {
  # TODO: Fix this in Config Adapter
  # Check univention-ssl/debian/univention-ssl.postinst
  # and make-certificates.sh
  target_dir="/etc/univention/ssl/ucs-6045.${DOMAIN_NAME}"
  mkdir --parents "${target_dir}" /etc/univention/ssl/ucsCA/

  ln --symbolic --force "${CA_CERT_FILE}" "/etc/univention/ssl/ucsCA/CAcert.pem"
  ln --symbolic --force "${CERT_PEM_FILE}" "${target_dir}/cert.pem"
  ln --symbolic --force "${PRIVATE_KEY_FILE}" "${target_dir}/private.key"

}

check_unset_variables
setup_symlinks
setup_paths
setup_listener_path
setup_last_id_path
setup_slapd_conf
setup_sasl_mech_whitelist
setup_sasl_mech_saml
setup_initial_ldif
setup_translog_ldif
setup_ssl_certificates

exec "$@"

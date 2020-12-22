FROM debian:buster-slim

SHELL ["/bin/bash", "-c"]

# dependencies
RUN \
  set -euxo pipefail && \
  echo 'debconf debconf/frontend select readline' | debconf-set-selections && \
  apt-get update && \
  apt-get --assume-yes --verbose-versions install ca-certificates curl gpg libterm-readline-gnu-perl

# postfix
RUN \
  set -euxo pipefail && \
  echo "postfix postfix/main_mailer_type string 'Satellite system'" | debconf-set-selections && \
  echo "postfix postfix/mailname string univention-directory-listener" | debconf-set-selections && \
  apt-get --assume-yes --verbose-versions install postfix

COPY sources.list /etc/apt/sources.list.d/15_ucs-online-version.list

# listener
RUN \
  set -euxo pipefail && \
  curl -fsSL https://updates.software-univention.de/univention-archive-key-ucs-4x.gpg | \
    apt-key add - && \
  echo "192.168.0.10 omar.knut.univention.de" >> /etc/hosts && \
  apt-get update && \
  apt-get --assume-yes --verbose-versions install univention-directory-listener

COPY ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

CMD [ \
  "-F", \
  "-d 2", \
  "-b ${LDAP_BASE_DN}", \
  "-m /usr/lib/univention-directory-listener/system", \
  "-c /var/lib/univention-directory-listener", \
  "-ZZ", \
  "-x", \
  "-D ${LDAP_BIND_DN}", \
  "-y /etc/ldap.secret" \
]

# [EOF]

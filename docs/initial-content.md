# Initial content

The content of the LDAP directory is initialized during the first start of the
container `ldap-server` through its `ENTRYPOINT` script.

The script loads the LDIF files which are also used in the join script of the
Debian package `univention-ldap`.


## Pointers

- The join script of the package `univention-ldap`:
  https://git.knut.univention.de/univention/ucs/-/blob/5.0-4/management/univention-ldap/01univention-ldap-server-init.inst

- The core LDIF file templates ``base.ldif`` and ``core-edition.ldif``:
  https://git.knut.univention.de/univention/ucs/-/tree/5.0-4/management/univention-ldap

- The documentation about join scripts:
  https://docs.software-univention.de/developer-reference/5.0/en/join/index.html

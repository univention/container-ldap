# Initial content

The content of the LDAP directory is initialized during the first start of the
container `ldap-server` through its `ENTRYPOINT` script.

The script loads the LDIF files which are also used in the join script of the
Debian package `univention-ldap`.


## Scaled deployments

In a scaled up deployment we ensure that the initial content is only loaded once
in the first primary server:

- `setup_initial_ldif` is only executed if the environment variable
  `LDAP_SERVER_ROLE` has the value `"primary"`.

- If `LDAP_SERVER_ENABLE_STATUS_CONFIGMAP` is enabled, then the initial content
  loading will be guarded by a `ConfigMap`, so that we ensure that only the
  first primary will load the initial content.

  This also guards against scenarios where the volume of the primary is reset.
  In this case it will not load initial content and start to replicate from the
  other primary instance.

  This feature depends on the Kubernetes API.


## Pointers

- The join script of the package `univention-ldap`:
  https://git.knut.univention.de/univention/ucs/-/blob/5.0-4/management/univention-ldap/01univention-ldap-server-init.inst

- The core LDIF file templates ``base.ldif`` and ``core-edition.ldif``:
  https://git.knut.univention.de/univention/ucs/-/tree/5.0-4/management/univention-ldap

- The documentation about join scripts:
  https://docs.software-univention.de/developer-reference/5.0/en/join/index.html

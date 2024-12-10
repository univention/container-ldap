# Environment variables

## Container `ldap-server`

### `LDAP_SERVER_ROLE` - Optional

Relevant in scaled deployments, by default the value `primary` is assumed.

This influences the loading of initial content into the directory.

Allowed values:

- `primary`

- `secondary`

- `proxy`


### `LDAP_SERVER_ENABLE_STATUS_CONFIGMAP` - Optional

Relevant in scaled deployments, by default the value `false` is assumed.

Enables the usage of a Kubernetes `ConfigMap` so keep track of status
information about the database initialization.

Allowed values:

- `true`

- `false`

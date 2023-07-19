# Containers for Univention LDAP

The repository does contain the following two containers:

- `ldap-server` runs OpenLDAP.
- `ldap-notifier` does run the Univention Directory Notifier.


## Start based on `docker compose`

The repository does include a compose file to start things up quickly. It will
start three services:

- `ldap-server` - The OpenLDAP server.
- `ldap-notifier` - The Univention Directory Notifier.
- `ldap-admin` - An instance of phpLDAPadmin as a web UI to access
  `ldap-server`.


To set it up:

1. Copy the `.env` file `.env.ldap-server.example` to `.env.ldap-server` and adjust
   as needed.

2. Bring up the services by running:

   ```
   docker compose up
   ```

The web UI is by default available at <http://localhost:8001>.



## Interacting with `ldap-server`


From the command line if you have the required tools available:

```
ldapwhoami -H ldap://localhost:389 -x -D cn=admin,dc=univention-organization,dc=intranet -w univention

ldapsearch -H ldap://localhost:389 -x -D cn=admin,dc=univention-organization,dc=intranet -w univention -b dc=univention-organization,dc=intranet
```


## Interacting with the `ldap-notifier`

One option is to connect the base listener to the running notifier, this does
involve manual tweaking at the moment though. The process is roughly as follows:

- Have the `container-listener-base` repository available and be able to run it
  via `docker compose`. Set the `.env.listener` according to your local
  containers.


## Manually testing a full round trip

The easiest way is to open phpLDAPadmin and change the description of the admin
user.

Have the `container-listener-base` and the services from this repository running.


1. Open the web UI, by default <http://localhost:8001>.

2. Log in, typically using `cn=admin,dc=univention-organization,dc=intranet` and
   the password matching your setting from the file `.env.ldap-server`.

3. Find the object `cn=admin,dc=univention=organization,dc=intranet`.

4. Add or change the attribute "description" and save the new value.

5. Don't forget to confirm that you want to change the value. ;-)

6. Observe that the `base-listener` logs details about the change. This means
   the change went into `ldap-server` and arrived in `ldap-notifier` and finally
   made its way to `base-listener`.


## Testing

The tests are grouped in the folder `./tests`. Details are described in the file
[`./tests/README.md`][tests_readme_md].

[tests_readme_md]: ./tests/README.md


## TLS

If TLS termination by the LDAP server is required,
you need to set `TLS_MODE=secure`
and provide the following secrets:
- `CA_CERT_FILE`: The CA certificate in PEM format.
- `CERT_PEM_FILE`: The server's (public) certificate in PEM format.
- `PRIVATE_KEY_FILE`: The private key to the server's certificate.
- `DH_PARAM_FILE`: Diffie-Hellman parameters.

The file `./generate-secrets.sh` can be used to generate a set of secrets.
Then enable the respective options in `.env.ldap-server`.

In order for clients to connect properly
- the CA certificate must also be known and trusted by the client,
- the LDAP server must be reachable by the hostname listed in its certificate.
  (Maybe Subject Alternative Names can be useful here.)

Setting `TLS_MODE` to `off` disables TLS support.
In this case, no certificate files need to be provided.

## Logging

The log level can be set through the `LOG_LEVEL` flag
as a comma-separated list of values found in the [OpenLDAP documentation](https://www.openldap.org/doc/admin24/runningslapd.html#Command-Line%20Options).

The default is `LOG_LEVEL=stats`.

## Notifier Data Files

### OpenLDAP translog output file

Location: `/var/lib/univention-ldap/listener/listener`

Needs to be shared between `ldap-server` and `ldap-notifier` container.
Lines get added by the `translog-slapd-overlay` on LDAP-Object change.
The notifier removes lines after processing them.

### Translog lock-file

Location: `/var/lib/univention-ldap/listener/listener.lock`

Needs to be shared between `ldap-server` and `ldap-notifier` container.
Created by the `entrypoint` script of the `ldap-server` container.
Written by the `translog-slapd-overlay` and the notifier.

### Processed notifier transactions (db)

Location: `/var/lib/univention-ldap/notify/transaction.index`

Written by the notifier.
Binary data.

### Notifier lock-file

Location: `/var/lib/univention-ldap/notify/transaction.lock`

Written by the notifier.

### Processed notifier transactions (flat file)

Location: `/var/lib/univention-ldap/notify/transaction`

Written by the notifier.
Contains transaction lines.
A line contains transaction-id, DN and change-type separated by space.

### Notifier log-file

Location: `/var/log/univention/notifier.log`

The log-path is hard-coded but should be configurable to use `stdout` instead.
See
`management/univention-directory-notifier/src/univention-directory-notifier.c`
in the ucs-repository!

### LDAP-API

Location: `/var/run/slapd/ldapi`

The notifier is hard-coded to connect via `ldapapi:///`.
Therefore the `ldapi` file needs to be shared from the OpenLDAP server container.

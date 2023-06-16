# Containers for Univention LDAP

The repository does contain the following two containers:

- `ldap-server` runs OpenLDAP.
- `ldap-notifier` does run the Univention Directory Notifier.


## Start based on `docker compose`

The repository does include a compose file to start things up quickly. It will
start three services:

- `ldap-server` - The OpenLDAP server.
- `ldap-notifier` - The Univention Directory Notifier.
- `ldap-admin` - An instance of phpldapadmin as a web ui to access
  `ldap-server`.


To set it up:

1. Copy the env file `.env.ldap-server.example` to `.env.ldap-server` and adjust
   as needed.

2. Bring up the services by running:

   ```
   docker compose up
   ```

The web ui is by default available at <http://localhost:8001>.



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


## Testing a full round trip

The easiest way is to open phpldapadmin and change the description of the admin
user.

Have the `container-listener-base` and the services from this repository running.


1. Open the web ui, by default <http://localhost:8001>.

2. Log in, typically using `cn=admin,dc=univention-organization,dc=intranet` and
   the password matching your hash from the file `.env.ldap-server`.

3. Find the object `cn=admin,dc=univention=organization,dc=intranet`.

4. Add or change the attribute "description" and save the new value.

5. Don't forget to confirm that you want to change the value. ;-)

6. Observe that the `base-listener` logs details about the change. This means
   the change went into `ldap-server` and arrived in `ldap-notifier` and finally
   made its way to `base-listener`.


## Preparation

### Diffie-Hellman Parameters

Generate your own DH-Parameters with:

   openssl dhparam -out "dh_2048.pem" -2 2048


### pre-commit hook

The pre-commit hook works with the `pre-commit` tool, which is configured
in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file.
It is recommended, that you [install the tool](
https://pre-commit.com/#installation) in your environment so it's execution
is automatically triggered when you invoke `git commit`.
Alternatively you can use the [pre-commit container image](
#pre-commit-container).

#### run container

Run pre-commit in the container:

    sudo mkdir --parents /root/.cache/pre-commit
    docker run \
      --mount type=bind,source=${PWD},target=/code \
      --mount type=bind,source=/root/.cache/pre-commit,target=/root/.cache/pre-commit \
      uv-pre-commit:container-ldap

#### Dependencies

##### GitLab CI linter

Currently the configuration contains the [GitLab CI linter](
https://gitlab.com/devopshq/gitlab-ci-linter) which needs access
to the [Univention GitLab instance](https://git.knut.univention.de/)
for linting the [CI configuration](.gitlab-ci.yml) itself.
Make sure that the environment in which you are running `pre-commit`, has the
certificate for `git.knut.univention.de` or consider using the
[pre-commit container image](#pre-commit-container),
which has the certificate built into it.


## Notifier Data Files

### OpenLDAP translog output file
Location: /var/lib/univention-ldap/listener/listener
Needs to be shared between ldap and notifier container.
Lines get added by the translog-slapd-overlay on LDAP-Object change.
The notifier removes lines after processing them.

### Translog lock-file
Location: /var/lib/univention-ldap/listener/listener.lock
Needs to be shared between ldap and notifier container.
Created by the entrypoint script of the ldap-container.
Written by the translog-slapd-overlay and the notifier.

### Processed notifier transactions (db)
Location: /var/lib/univention-ldap/notify/transaction.index
Written by the notfier.
Binary data.

### Notifier lock-file
Location: /var/lib/univention-ldap/notify/transaction.lock
Written by the notfier.

### Processed notifier transactions (flat file)
Location: /var/lib/univention-ldap/notify/transaction
Written by the notfier.
Contains transaction lines.
A line contains transaction-id, DN and change-type separated by space.

### Notifier log-file
Location: /var/log/univention/notifier.log
The log-path is hard-coded but should be configurable to use stdout instead.
See
`management/univention-directory-notifier/src/univention-directory-notifier.c`
in the ucs-repository!

### LDAP-API
Location: /var/run/slapd/ldapi
The notifier is hard-coded to connect via "ldapapi:///".
Therefore the ldapi file needs to be shared from the OpenLDAP server container.

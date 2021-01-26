Containers for Univention LDAP

## Preparation

### Allow connections to the UV-internal docker-registry

#### Either Install the UCS-Root-Cert for docker-pull:

    sudo mkdir --parents /etc/docker/certs.d/docker-registry.knut.univention.de
    sudo wget --no-check-certificate --output-document=/etc/docker/certs.d/docker-registry.knut.univention.de/CA.crt https://billy.knut.univention.de/ucs-root-ca.crt


#### Or configure docker client to skip SSL

Alternatively you open /etc/docker/daemon.json and add/edit the line
    "insecure-registries" : [ "docker-registry.knut.univention.de" ],


### Diffie-Hellman Parameters

Generate your own DH-Parameters with:

   openssl dhparam -out "dh_2048.pem" -2 2048


### pre-commit hook

The pre-commit hook work with the `pre-commit` tool, which is configured
in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file.
It is recommended, that you [install the tool](
https://pre-commit.com/#installation) in your environment so it's execution
is automatically triggered when you invoke `git commit`.
Alternatively you can use the [pre-commit container image](
#pre-commit-container).

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


#### pre-commit container

Build the container image with:

    docker build --tag pre-commit:container-ldap images/pre-commit/

Run pre-commit in the container:

    sudo mkdir --parents /root/.cache/pre-commit
    docker run \
      --mount type=bind,source=${PWD},target=/code \
      --mount type=bind,source=/root/.cache/pre-commit,target=/root/.cache/pre-commit \
      pre-commit:container-ldap

## Notifier Data Files

### OpenLDAP translog output file
Location: /var/lib/univention-ldap/listener/listener
Needs to be shared between ldap and notifier container.
Written by the translog slapd overlay on LDAP-Object change.
Read by the notifier.

### Translog lock-file
Location: /var/lib/univention-ldap/listener/listener.lock
Created by slapd but needs to be writeable by the notifier.
Empty.

### Processed notifier transactions (db)
Location: /var/lib/univention-ldap/notify/transaction.index
Written by the notfier.
Binary date.

### Notifier lock-file
Location: /var/lib/univention-ldap/notify/transaction.lock
Written by the notfier.
Empty.

### Processed notifier transactions (flat file)
Location: /var/lib/univention-ldap/notify/transaction
Written by the notfier.
Contains transaction lines.
A line contains transaction-id, DN and change-type separated by space.

### Notifier log-file
Location: /var/log/univention/notifier.log
Written by the notfier.

### LDAP-API
Location: /var/run/slapd/ldapi
The notifier is hardcoded to connect via "ldapapi:///".
Therefore the ldapi file needs to be shared from the OpenLDAP server container.

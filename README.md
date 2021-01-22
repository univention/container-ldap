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

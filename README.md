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
https://gitlab.com/devopshq/gitlab-ci-linter)
so it is recommended that you `export GITLAB_PRIVATE_TOKEN=<YOUR_TOKEN_HERE>`
after you create your [personal access token](
https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-tokens)
. If you can't do that right now, and you would rather run the rest of the
linters, then you can skip that linter by setting the `SKIP` variable like
`SKIP=gitlab-ci-linter pre-commit run --all-files`.


#### pre-commit container

Build the container image with:

    docker build --tag pre-commit:container-ldap images/pre-commit/

Run pre-commit in the container:

    sudo mkdir --parents /root/.cache/pre-commit
    docker run \
      --env GITLAB_PRIVATE_TOKEN \
      --mount type=bind,source=${PWD},target=/code \
      --mount type=bind,source=/root/.cache/pre-commit,target=/root/.cache/pre-commit \
      pre-commit:container-ldap

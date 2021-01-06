Containers for Univention LDAP

## Preparation

### Allow connections to the UV-internal docker-registry

#### Either Install the UCS-Root-Cert for docker-pull:

    sudo mkdir --parents /etc/docker/certs.d/docker-registry.knut.univention.de
    sudo wget --no-check-certificate --output-document=/etc/docker/certs.d/docker-registry.knut.univention.de/CA.crt https://billy.knut.univention.de/ucs-root-ca.crt


#### Or configure docker client to skip SSL

Alternatively you open /etc/docker/daemon.json and add/edit the line
    "insecure-registries" : [ "docker-registry.knut.univention.de" ],


#### Diffie-Hellman Parameters

Generate your own DH-Parameters with:

   openssl dhparam -out "dh_2048.pem" -2 2048


#### pre-commit container

Build the container with:

    docker build --tag pre-commit:container-ldap images/pre-commit/

Run pre-commit:

    sudo mkdir --parents /root/.cache/pre-commit
    docker run \
      --mount type=bind,source=${PWD},target=/code \
      --mount type=bind,source=/root/.cache/pre-commit,target=/root/.cache/pre-commit \
      pre-commit:container-ldap

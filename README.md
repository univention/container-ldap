
Containers for Univention LDAP

### Preparation

Install the UCS-Root-Cert for docker-pull:

    sudo mkdir --parents /etc/docker/certs.d/docker-registry.knut.univention.de
    sudo wget --no-check-certificate --output-document=/etc/docker/certs.d/docker-registry.knut.univention.de/CA.crt https://billy.knut.univention.de/ucs-root-ca.crt

#### Diffie-Hellman Parameters

Generate your own DH-Parameters with:

   openssl dhparam -out "dh_2048.pem" -2 2048

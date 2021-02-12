#!/usr/bin/env bash

docker build -f Dockerfile_SIMPLE_SAML \
    -t artifacts.knut.univention.de/upx/container-ldap/acceptance_test/simple_saml:base \
    . || exit 1

docker build -f Dockerfile_SAML_SP \
    -t artifacts.knut.univention.de/upx/container-ldap/acceptance_test/saml_sp:latest \
    . || exit 1

docker build -f Dockerfile_SAML_IdP \
    -t artifacts.knut.univention.de/upx/container-ldap/acceptance_test/saml_idp:latest \
    . || exit 1

for image in \
    artifacts.knut.univention.de/upx/container-ldap/acceptance_test/simple_saml:latest \
    artifacts.knut.univention.de/upx/container-ldap/acceptance_test/saml_sp:latest \
    artifacts.knut.univention.de/upx/container-ldap/acceptance_test/saml_idp:latest \
    ; do docker push ${image}; done

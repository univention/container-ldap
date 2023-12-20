#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH


# define hostname to be signed
hostname=localhost

mkdir -p ssl

#########################################
# Generate CA certificate
openssl genrsa \
    -out ssl/CAcert.key \
    4096
openssl req \
    -new \
    -x509 \
    -key ssl/CAcert.key \
    -out ssl/CAcert.pem \
    -subj "/C=DE/ST=Bremen/L=Bremen/O=Fake Corporation/OU=Souvereign Workplace/CN=Souvereign Workplace Root CA/emailAddress=root@example.org"

#########################################
# Generate server certificate
openssl genrsa \
    -out ssl/cert.key \
    4096
openssl req \
    -new \
    -key ssl/cert.key \
    -out ssl/cert.csr \
    -subj "/C=DE/ST=Bremen/L=Bremen/O=Fake Corporation/OU=Souvereign Workplace/CN=${hostname}/emailAddress=root@example.org"
openssl x509 \
    -req \
    -in ssl/cert.csr \
    -CA ssl/CAcert.pem \
    -CAkey ssl/CAcert.key \
    -CAcreateserial \
    -out ssl/cert.pem
rm ssl/cert.csr

#########################################
# Generate Diffie-Hellman parameters
openssl dhparam \
    -2 \
    -out ssl/dh_2048.pem \
    2048

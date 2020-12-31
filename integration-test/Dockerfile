FROM python:3.7-alpine

RUN apk update && apk --no-cache add bash openldap-clients && rm -rf /var/cache/apk/*

COPY tests/ldap_test.sh /

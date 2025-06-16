# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest
from test_deployment import ContainerAuthFromExistingSecret

from univention.testing.helm.deployment import DeploymentTlsDhparamVolumeSecret, DeploymentTlsVolumeSecret


@pytest.mark.parametrize(
    "key, env_var",
    [
        ("ldapServer", "LDAP_CN_ADMIN_PW"),
        ("ldapServer", "SYNC_PASSWORD"),
    ],
)
class TestStatefulSet01LdapServerAuthFromExistingSecret(ContainerAuthFromExistingSecret):
    template_file = "templates/statefulset-primary.yaml"
    container_name = "openldap"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, volume_item",
    [
        ("ldapServer.tls", "ca.crt"),
        ("ldapServer.tls", "tls.crt"),
        ("ldapServer.tls", "tls.key"),
    ],
)
class TestStatefulSet01LdapTlsVolumesFromExistingSecret(DeploymentTlsVolumeSecret):
    template_file = "templates/statefulset-primary.yaml"
    volume_name = "release-name-ldap-server-tls-volume"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, volume_item",
    [
        ("ldapServer.tls.dhparam", "dhparam.pem"),
    ],
)
class TestStatefulSet01LdapTlsDhparamVolumesFromExistingSecret(DeploymentTlsDhparamVolumeSecret):
    template_file = "templates/statefulset-primary.yaml"
    volume_name = "release-name-ldap-server-dh-volume"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, env_var",
    [
        ("ldapServer", "LDAP_CN_ADMIN_PW"),
        ("ldapServer", "SYNC_PASSWORD"),
    ],
)
class TestStatefulSet02LdapServerAuthFromExistingSecret(ContainerAuthFromExistingSecret):
    template_file = "templates/statefulset-secondary.yaml"
    container_name = "openldap"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, volume_item",
    [
        ("ldapServer.tls", "ca.crt"),
        ("ldapServer.tls", "tls.crt"),
        ("ldapServer.tls", "tls.key"),
    ],
)
class TestStatefulSet02LdapTlsVolumesFromExistingSecret(DeploymentTlsVolumeSecret):
    template_file = "templates/statefulset-secondary.yaml"
    volume_name = "release-name-ldap-server-tls-volume"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, volume_item",
    [
        ("ldapServer.tls.dhparam", "dhparam.pem"),
    ],
)
class TestStatefulSet02LdapTlsDhparamVolumesFromExistingSecret(DeploymentTlsDhparamVolumeSecret):
    template_file = "templates/statefulset-secondary.yaml"
    volume_name = "release-name-ldap-server-dh-volume"
    chart_name = "ldap-server"

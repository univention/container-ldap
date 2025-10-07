# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest

from univention.testing.helm.deployment import DeploymentTlsDhparamVolumeSecret, DeploymentTlsVolumeSecret


@pytest.mark.parametrize(
    "key, volume_item",
    [
        ("ldapServer.tls", "ca.crt"),
        ("ldapServer.tls", "tls.crt"),
        ("ldapServer.tls", "tls.key"),
    ],
)
class TestMainContainerLdapTlsVolumesFromExistingSecret(DeploymentTlsVolumeSecret):
    template_file = "templates/deployment-proxy.yaml"
    volume_name = "release-name-ldap-server-tls-volume"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, volume_item",
    [
        ("ldapServer.tls.dhparam", "dhparam.pem"),
    ],
)
class TestMainContainerLdapTlsDhparamVolumesFromExistingSecret(DeploymentTlsDhparamVolumeSecret):
    template_file = "templates/deployment-proxy.yaml"
    volume_name = "release-name-ldap-server-dh-volume"
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

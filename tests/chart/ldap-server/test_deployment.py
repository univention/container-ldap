# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest
from pytest_helm.utils import add_jsonpath_prefix, findone, load_yaml

from univention.testing.helm.container import ContainerEnvVarSecret
from univention.testing.helm.deployment import DeploymentTlsDhparamVolumeSecret, DeploymentTlsVolumeSecret


class ContainerAuthFromExistingSecret(ContainerEnvVarSecret):
    chart_name = ""

    def test_auth_disabling_existing_secret(self, helm, chart_path, key, env_var):
        values = add_jsonpath_prefix(
            key,
            load_yaml(
                """
                auth:
                  existingSecret: null
            """,
            ),
        )
        container_type = "initContainers" if self.container_is_init else "containers"
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.{container_type}[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        # assert env["valueFrom"]["secretKeyRef"]["name"].startswith(self.secret_name_default)
        assert env["valueFrom"]["secretKeyRef"]["name"].startswith(
            f"release-name-{self.chart_name}",
        )
        assert env["valueFrom"]["secretKeyRef"]["key"] == "password"


@pytest.mark.parametrize(
    "key, env_var",
    [
        ("ldapServer", "LDAP_CN_ADMIN_PW"),
    ],
)
class TestMainContainerLdapServerAuthFromExistingSecret(ContainerAuthFromExistingSecret):
    template_file = "templates/deployment-proxy.yaml"
    container_name = "main"
    chart_name = "ldap-server"


@pytest.mark.parametrize(
    "key, env_var",
    [
        ("ldapServer", "LDAP_CN_ADMIN_PW"),
    ],
)
class TestInitContainerLdapServerAuthFromExistingSecret(ContainerAuthFromExistingSecret):
    template_file = "templates/deployment-proxy.yaml"
    container_name = "wait-for-secondary"
    chart_name = "ldap-server"
    container_is_init = True


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

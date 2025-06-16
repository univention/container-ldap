# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest
from pytest_helm.utils import add_jsonpath_prefix, findone, load_yaml

from univention.testing.helm.base import Base
from univention.testing.helm.container import ContainerEnvVarSecret


@pytest.mark.parametrize(
    "key, env_var",
    [
        ("ldapServer", "LDAP_CN_ADMIN_PW"),
        ("ldapServer", "SYNC_PASSWORD"),
    ],
)
class TestStatefulSet01LdifLdapAuthFromExistingSecret(ContainerEnvVarSecret):
    template_file = "templates/statefulset-primary.yaml"
    container_name = "ldif-producer"

    def test_auth_disabling_existing_secret(self, helm, chart_path, key, env_var):
        # TODO: Since automatic secret creation is not implemented for ldap-server,
        # this test is not applicable
        pass


@pytest.mark.parametrize(
    "key, env_var",
    [
        ("ldifProducer.nats", "NATS_USERNAME"),
        ("ldifProducer.nats", "NATS_PASSWORD"),
    ],
)
class TestStatefulSet01LdifNatsAuthFromExistingSecret(Base):
    template_file = "templates/statefulset-primary.yaml"
    container_name = "ldif-producer"
    container_is_init = False

    def test_auth_existing_secret_custom_name(
        self,
        helm,
        chart_path,
        key,
        env_var,
    ):
        values = add_jsonpath_prefix(
            key,
            load_yaml(
                """
                auth:
                  existingSecret:
                    name: "stub-secret-name"
            """,
            ),
        )
        container_type = "initContainers" if self.container_is_init else "containers"
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.{container_type}[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == env_var

    def test_auth_existing_secret_custom_key(
        self,
        helm,
        chart_path,
        key,
        env_var,
    ):
        values = add_jsonpath_prefix(
            key,
            load_yaml(
                f"""
                auth:
                  existingSecret:
                    name: "stub-secret-name"
                    keyMapping:
                      {env_var}: "stub_password_key"
            """,
            ),
        )
        container_type = "initContainers" if self.container_is_init else "containers"
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = findone(
            deployment,
            f"spec.template.spec.{container_type}[?@.name=='{self.container_name}'].env[?@.name=='{env_var}']",
        )
        assert env["valueFrom"]["secretKeyRef"]["name"] == "stub-secret-name"
        assert env["valueFrom"]["secretKeyRef"]["key"] == "stub_password_key"

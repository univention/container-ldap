# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest

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

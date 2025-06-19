# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from univention.testing.helm.client.ldap import Auth, AuthViaEnv, AuthOwner


class TestPrimaryAuth(AuthOwner, AuthViaEnv, Auth):
    config_map_name = "release-name-ldap-server"
    secret_name = "release-name-ldap-server-ldap"
    workload_kind = "StatefulSet"
    workload_name = "release-name-ldap-server-primary"

    sub_path_env_password = "env[?@.name=='LDAP_CN_ADMIN_PW']"

    derived_password = "751120bf3b933a18b7d637bfba5e9389939c4bbd"

    prefix_mapping = {
        "ldapServer.auth": "ldap.auth",
    }

    @pytest.mark.skip(reason="TODO: Decide if bindDn is configurable.")
    def test_auth_plain_values_provide_bind_dn():
        pass

    @pytest.mark.skip(reason="TODO: Decide if bindDn is configurable.")
    def test_auth_plain_values_bind_dn_is_templated():
        pass

    @pytest.mark.skip(reason="TODO: Decide if bindDn is configurable.")
    def test_auth_bind_dn_is_required():
        pass

    @pytest.mark.skip(reason="TODO: Decide if bindDn is configurable.")
    def test_auth_bind_dn_has_default():
        pass


class TestPrimaryAuthSyncPassword(TestPrimaryAuth):
    sub_path_env_password = "env[?@.name=='SYNC_PASSWORD']"


class TestSecondaryAuth(TestPrimaryAuth):
    workload_name = "release-name-ldap-server-secondary"


class TestSecondaryAuthSyncPassword(TestSecondaryAuth):
    sub_path_env_password = "env[?@.name=='SYNC_PASSWORD']"


class TestSecondaryAuthWaitForPrimary(TestSecondaryAuth):
    path_main_container = "..spec.template.spec.initContainers[?@.name=='wait-for-primary']"


class TestSecondaryAuthWithForPrimarySyncPassword(TestSecondaryAuthWaitForPrimary):
    sub_path_env_password = "env[?@.name=='SYNC_PASSWORD']"


class TestProxyAuth(TestPrimaryAuth):
    workload_kind = "Deployment"
    workload_name = "release-name-ldap-server-proxy"


class TestProxyAuthWaitForSecondary(TestProxyAuth):
    path_main_container = "..spec.template.spec.initContainers[?@.name=='wait-for-secondary']"

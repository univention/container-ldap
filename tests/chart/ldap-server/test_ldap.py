# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from univention.testing.helm.client.ldap import LdapAuth, LdapAuthUsageViaEnv


class TestPrimaryAuth(LdapAuthUsageViaEnv, LdapAuth):
    config_map_name = "release-name-ldap-server"
    secret_name = "release-name-ldap-server-ldap"
    workload_kind = "StatefulSet"
    workload_name = "release-name-ldap-server-primary"

    sub_path_env_password = "env[?@.name=='LDAP_CN_ADMIN_PW']"

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


class TestPrimaryLdifProducerAuth(TestPrimaryAuth):

    path_main_container = "..spec.template.spec.containers[?@.name=='ldif-producer']"


class TestPrimaryAuthSyncPassword(TestPrimaryAuth):
    sub_path_env_password = "env[?@.name=='SYNC_PASSWORD']"


class TestPrimaryLdifProducerAuthSyncPassword(TestPrimaryLdifProducerAuth):

    path_main_container = "..spec.template.spec.containers[?@.name=='ldif-producer']"
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

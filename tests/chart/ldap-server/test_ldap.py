# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client.ldap import AuthOwner, AuthPassword, AuthViaEnv


class TestPrimaryAuth(AuthOwner, AuthViaEnv, AuthPassword):
    config_map_name = "release-name-ldap-server"
    secret_name = "release-name-ldap-server-ldap"
    workload_kind = "StatefulSet"
    workload_name = "release-name-ldap-server-primary"

    sub_path_env_password = "env[?@.name=='LDAP_CN_ADMIN_PW']"

    derived_password = "2668ce471617b34ead65e1650fea7220577e6bc6"

    prefix_mapping = {
        "ldapServer.auth": "ldap.auth",
    }


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

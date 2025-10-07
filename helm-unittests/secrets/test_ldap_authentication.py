# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import AuthSecretGenerationOwner


class SettingsTestLdapSecret:
    secret_name = "release-name-ldap-server-admin"
    prefix_mapping = {"ldapServer.auth": "auth"}


class TestChartCreatesLdapSecretAsOwner(SettingsTestLdapSecret, AuthSecretGenerationOwner):
    derived_password = "2668ce471617b34ead65e1650fea7220577e6bc6"


class TestProxyUsesLdapCredentialsByEnv(SettingsTestLdapSecret, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='LDAP_CN_ADMIN_PW']"
    workload_name = "release-name-ldap-server-proxy"
    workload_kind = "Deployment"


class TestPrimaryUsesLdapCredentialsByEnv(SettingsTestLdapSecret, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='LDAP_CN_ADMIN_PW']"
    workload_name = "release-name-ldap-server-primary"
    workload_kind = "StatefulSet"


class TestPrimaryUsesLdapCredentialsByEnvForSync(SettingsTestLdapSecret, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='SYNC_PASSWORD']"
    workload_name = "release-name-ldap-server-primary"
    workload_kind = "StatefulSet"


class TestSecondaryUsesLdapCredentialsByEnv(SettingsTestLdapSecret, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='LDAP_CN_ADMIN_PW']"
    workload_name = "release-name-ldap-server-secondary"
    workload_kind = "StatefulSet"


class TestSecondaryUsesLdapCredentialsByEnvForSync(SettingsTestLdapSecret, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='SYNC_PASSWORD']"
    workload_name = "release-name-ldap-server-secondary"
    workload_kind = "StatefulSet"

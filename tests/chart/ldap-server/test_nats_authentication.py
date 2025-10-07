# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import AuthSecretGenerationUser
from univention.testing.helm.auth_flavors.username import AuthUsernameViaConfigMap
from univention.testing.helm.client.nats import Connection, ConnectionViaConfigMap


class SettingsTestNatsSecret:
    secret_name = "release-name-ldap-server-nats"
    prefix_mapping = {"ldifProducer.nats.auth": "auth"}

    # for AuthPasswordUsageViaEnv
    workload_name = "release-name-ldap-server-primary"
    workload_kind = "StatefulSet"


class TestChartCreatesNatsSecretAsUser(SettingsTestNatsSecret, AuthSecretGenerationUser):
    pass


class TestPrimaryLdapServerUsesNatsPasswordViaEnv(SettingsTestNatsSecret, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='NATS_PASSWORD']"
    path_container = "..spec.template.spec.containers[?@.name=='ldif-producer']"


class TestLdapServerUsesNatsUsernameViaConfigMap(SettingsTestNatsSecret, AuthUsernameViaConfigMap):
    config_map_name = "release-name-ldap-server-ldif-producer-config"
    path_username = "data.NATS_USERNAME"
    default_username = "ldif-producer"


class TestConnection(ConnectionViaConfigMap, Connection):
    config_map_name = "release-name-ldap-server-ldif-producer-config"

    prefix_mapping = {
        "ldifProducer.nats": "nats",
    }

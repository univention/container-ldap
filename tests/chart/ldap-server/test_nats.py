# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise

from univention.testing.helm.client.nats import (
    Auth,
    Connection,
    ConnectionViaConfigMap,
    SecretUsageViaEnv,
)


class TestAuth(SecretUsageViaEnv, Auth):
    config_map_name = "release-name-ldap-server-ldif-producer-config"
    workload_kind = "StatefulSet"
    workload_name = "release-name-ldap-server-primary"
    secret_name = "release-name-ldap-server-nats"

    default_username = "ldif-producer"

    path_main_container = "spec.template.spec.containers[?@.name=='ldif-producer']"

    prefix_mapping = {
        "ldifProducer.nats": "nats",
    }

    def test_auth_config_is_not_required_when_disabled(self, chart):
        values = self.load_and_map(
            """
            ldifProducer:
              enabled: false

              nats:
                auth:
                  username: null
                  password: null
            """
        )
        with does_not_raise():
            chart.helm_template(values)


class TestConnection(ConnectionViaConfigMap, Connection):
    config_map_name = "release-name-ldap-server-ldif-producer-config"

    prefix_mapping = {
        "ldifProducer.nats": "nats",
    }

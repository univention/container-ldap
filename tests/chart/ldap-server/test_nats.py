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


class TestConnection(ConnectionViaConfigMap, Connection):

    config_map_name = "release-name-ldap-server-ldif-producer-config"

    prefix_mapping = {
        "ldifProducer.nats": "nats",
    }

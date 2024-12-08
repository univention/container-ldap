from unittest import mock

import pytest


def test_uses_configuration_from_settings(evaluate_database_init, mocker):
    client_mock = mocker.patch.object(evaluate_database_init, "client")
    mocker.patch.dict(evaluate_database_init.settings, {
        "configmap": "stub_configmap", "namespace": "stub_namespace",
    })
    stub_configmap = mock.Mock()
    stub_configmap.data = {"ldap_database_initialized": "false"}
    read_namespaced_config_map_mock = client_mock.CoreV1Api().read_namespaced_config_map
    read_namespaced_config_map_mock.return_value = stub_configmap
    replace_namespaced_config_map_mock = client_mock.CoreV1Api().replace_namespaced_config_map

    evaluate_database_init.database_initialized()

    assert stub_configmap.data["ldap_database_initialized"] == "true"
    replace_namespaced_config_map_mock.assert_called_once_with(
        name="stub_configmap", namespace="stub_namespace", body=stub_configmap)

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

    with pytest.raises(SystemExit) as exit_info:
        evaluate_database_init.database_needs_initialization()

    assert exit_info.value.code == 0
    read_namespaced_config_map_mock.assert_called_once_with(
        name="stub_configmap", namespace="stub_namespace")

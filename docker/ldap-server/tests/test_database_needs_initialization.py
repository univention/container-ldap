from unittest import mock

import pytest


def test_uses_configuration_from_settings(evaluate_database_init, stub_settings, client_mock):
    stub_configmap = mock.Mock()
    stub_configmap.data = {"ldap_database_initialized": "uninitialized"}
    read_namespaced_config_map_mock = client_mock.CoreV1Api().read_namespaced_config_map
    read_namespaced_config_map_mock.return_value = stub_configmap

    evaluate_database_init.database_needs_initialization()

    read_namespaced_config_map_mock.assert_called_once_with(
        name="stub_configmap", namespace="stub_namespace")


def test_exit_code_1_if_already_initialized(evaluate_database_init, stub_settings, client_mock):
    stub_configmap = mock.Mock()
    stub_configmap.data = {"ldap_database_initialized": "initialized"}
    read_namespaced_config_map_mock = client_mock.CoreV1Api().read_namespaced_config_map
    read_namespaced_config_map_mock.return_value = stub_configmap

    with pytest.raises(SystemExit) as exit_info:
        evaluate_database_init.database_needs_initialization()

    assert exit_info.value.code == 1

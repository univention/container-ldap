import pytest


def test_discovers_namespace_as_fallback(evaluate_database_init, mocker):
    mocker.patch.object(evaluate_database_init, "configure_kubernetes_client")
    dn_mock = mocker.patch.object(
        evaluate_database_init, "discover_namespace", return_value="stub_namespace")

    evaluate_database_init.prepare_app()
    dn_mock.assert_called_once()
    assert evaluate_database_init.settings["namespace"] == "stub_namespace"


def test_uses_provided_namespace(evaluate_database_init, mocker):
    mocker.patch.object(evaluate_database_init, "configure_kubernetes_client")
    dn_mock = mocker.patch.object(evaluate_database_init, "discover_namespace")

    evaluate_database_init.prepare_app(namespace="stub_namespace")
    dn_mock.assert_not_called()
    assert evaluate_database_init.settings["namespace"] == "stub_namespace"

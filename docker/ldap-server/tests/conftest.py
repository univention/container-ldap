# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import importlib.util
import os

import pytest


@pytest.fixture
def evaluate_database_init():
    """Provide "evaluate_database_init.py" as a module."""
    module_name = "evaluate_database_init"
    module_path = "./evaluate_database_init.py"
    spec = importlib.util.spec_from_file_location(
        module_name,
        os.path.join(module_path),
    )
    if not (spec and spec.loader):
        raise RuntimeError("Loading the script as module did fail")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def stub_settings(evaluate_database_init, mocker):
    """
    Mock settings with a stub configuration.

    It does provide access to the injected settings as a `dict`.
    """
    settings = {
        "configmap": "stub_configmap",
        "namespace": "stub_namespace",
    }
    mocker.patch.dict(evaluate_database_init.settings, settings)
    return settings


@pytest.fixture
def client_mock(evaluate_database_init, mocker):
    """Mock of the Kubernetes client module."""
    return mocker.patch.object(evaluate_database_init, "client")

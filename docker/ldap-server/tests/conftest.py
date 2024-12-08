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

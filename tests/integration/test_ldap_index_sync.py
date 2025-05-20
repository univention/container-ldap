# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2024 Univention GmbH
import re

import pytest


def test_univention_object_identifier(log_file_path):
    if log_file_path.is_file():
        with log_file_path.open("r") as f:
            file_content = f.read()
            pattern = re.compile(r"Empty persistent volume. New state file with current state created.")
            new_state_file = bool(pattern.search(file_content))

            assert new_state_file

    else:
        pytest.skip("Logfile doesn't exists!")

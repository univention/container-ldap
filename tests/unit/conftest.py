# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from unittest import mock

import pytest

from univention.provisioning.ldif_producer.port import LDIFProducerMQPort


@pytest.fixture
def mock_message_queue_port() -> LDIFProducerMQPort:
    return mock.AsyncMock()

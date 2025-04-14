# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2025 Univention GmbH

from unittest import mock

import pytest

from univention.ldif_producer.mq_port import LDIFProducerMQPort


@pytest.fixture
def mock_message_queue_port() -> LDIFProducerMQPort:
    return mock.AsyncMock()

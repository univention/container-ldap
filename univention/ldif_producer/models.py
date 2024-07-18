# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from enum import Enum
from typing import NamedTuple

from ldap0.typehints import EntryMixed


class RequestType(str, Enum):
    add = "ADD"
    modify = "MODIFY"
    modrdn = "MODRDN"
    delete = "DELETE"


class LDAPMessage(NamedTuple):
    request_type: RequestType
    binddn: str
    message_id: int
    request_id: str
    old: EntryMixed | None
    new: EntryMixed | None

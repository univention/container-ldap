# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2024 Univention GmbH

import pytest
from ldap3 import ObjectDef, Writer


class MissingPortalExtension(Exception): ...


# We cannot use SKIP, because testing for LDAP schema requires opening a connection,
# which we don't want to do at import time. So we're using XFAIL at runtime instead.
# The test will still be reported as a regular failure if it raises anything else than
# MissingPortalExtension.


@pytest.mark.timeout(1)
@pytest.mark.xfail(raises=MissingPortalExtension, reason="Missing Portal Extension")
def test_create_portal_entry(connection, container, object_class_is_loaded):
    if not object_class_is_loaded("univentionNewPortalEntry"):
        raise MissingPortalExtension

    portal_entry = ObjectDef(["univentionNewPortalEntry"], connection)
    writer = Writer(connection, portal_entry)

    entry = writer.new("cn=test-portal-entry," + container.entry_dn)
    assert writer.commit()

    entry.entry_delete()
    assert writer.commit()


@pytest.mark.timeout(1)
@pytest.mark.xfail(raises=MissingPortalExtension, reason="Missing Portal Extension")
def test_create_portal_announcement(connection, container, object_class_is_loaded):
    if not object_class_is_loaded("univentionNewPortalAnnouncement"):
        raise MissingPortalExtension

    portal_announcement = ObjectDef(
        ["univentionNewPortalAnnouncement"],
        connection,
    )
    writer = Writer(connection, portal_announcement)

    announcement = writer.new(
        "cn=test-portal-announcement," + container.entry_dn,
    )
    assert writer.commit()

    announcement.entry_delete()
    assert writer.commit()

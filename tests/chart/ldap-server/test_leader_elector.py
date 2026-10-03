# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

from univention.testing.helm.base import Base

DATA_MOUNT = "volumeMounts[?@.mountPath=='/var/lib/univention-ldap']"


class TestLeaderElector(Base):
    template_file = "templates/statefulset-primary.yaml"

    def test_leader_elector_mounts_the_ldap_data_read_only(self, helm, chart_path):
        statefulset = self.helm_template_file(helm, chart_path, {}, self.template_file)

        elector = statefulset.findone("spec.template.spec.containers[?@.name=='leader-elector']")
        main = statefulset.findone("spec.template.spec.containers[?@.name=='main']")

        assert elector.findone(DATA_MOUNT)["readOnly"] is True
        assert not main.findone(DATA_MOUNT).get("readOnly", False)

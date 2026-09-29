# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import findone

from univention.testing.helm.base import Base


class TestPrimaryNotifierAffinity(Base):
    """
    Tests to ensure the LDAP primary and notifier pods remain co-located.

    The ldap-notifier has a hard affinity to the primary pod (required scheduling),
    which requires the primary to have a matching soft affinity preference to stay
    on the same node. Without this, the primary could be rescheduled elsewhere,
    breaking the shared-volume dependency.
    """

    def test_primary_prefers_notifier_node(self, helm, chart_path):
        result = self.helm_template_file(helm, chart_path, {}, "templates/statefulset-primary.yaml")
        term = findone(
            result,
            "spec.template.spec.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm",
        )
        assert term["topologyKey"] == "kubernetes.io/hostname"
        assert term["labelSelector"]["matchExpressions"] == [
            {"key": "app.kubernetes.io/name", "operator": "In", "values": ["ldap-notifier"]},
        ]

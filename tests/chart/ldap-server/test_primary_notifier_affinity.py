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

    def test_primary_has_pod_affinity_to_notifier(self, helm, chart_path):
        """Verify the primary has a soft affinity preference toward the notifier."""
        deployment = self.helm_template_file(helm, chart_path, {}, "templates/statefulset-primary.yaml")

        pod_affinity = findone(
            deployment,
            "spec.template.spec.affinity.podAffinity",
        )

        assert pod_affinity is not None, "Primary must have podAffinity toward the notifier"

    def test_primary_pod_affinity_targets_notifier(self, helm, chart_path):
        """Verify the podAffinity targets the ldap-notifier by app.kubernetes.io/name label."""
        deployment = self.helm_template_file(helm, chart_path, {}, "templates/statefulset-primary.yaml")

        match_expressions = findone(
            deployment,
            "spec.template.spec.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions",
        )

        assert match_expressions is not None, "podAffinity must have label selectors"
        assert len(match_expressions) > 0, "Must have at least one label selector"

        notifier_selector = next(
            (expr for expr in match_expressions if expr.get("key") == "app.kubernetes.io/name"),
            None,
        )
        assert notifier_selector is not None, "Must target app.kubernetes.io/name label"
        assert notifier_selector.get("operator") == "In"
        assert "ldap-notifier" in notifier_selector.get("values", [])

    def test_primary_pod_affinity_uses_hostname_topology(self, helm, chart_path):
        """Verify the affinity uses kubernetes.io/hostname as topologyKey."""
        deployment = self.helm_template_file(helm, chart_path, {}, "templates/statefulset-primary.yaml")

        topology_key = findone(
            deployment,
            "spec.template.spec.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey",
        )

        assert topology_key == "kubernetes.io/hostname", "Must use kubernetes.io/hostname to bind to same node"

    def test_primary_pod_affinity_is_soft_not_hard(self, helm, chart_path):
        """
        Verify the affinity is preferred (soft), not required (hard).

        Using required scheduling would block the primary on fresh installs where
        the notifier doesn't exist yet.
        A preference allows co-location when possible
        without blocking initial deployment.
        """
        deployment = self.helm_template_file(helm, chart_path, {}, "templates/statefulset-primary.yaml")

        # Soft affinity uses preferredDuringSchedulingIgnoredDuringExecution
        preferred_affinity = findone(
            deployment,
            "spec.template.spec.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution",
        )

        # Hard affinity uses requiredDuringSchedulingIgnoredDuringExecution
        required_affinity = findone(
            deployment,
            "spec.template.spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution",
        )

        assert preferred_affinity is not None and len(preferred_affinity) > 0, (
            "podAffinity must use preferredDuringSchedulingIgnoredDuringExecution"
        )
        assert required_affinity is None or len(required_affinity) == 0, (
            "podAffinity must NOT use requiredDuringSchedulingIgnoredDuringExecution"
        )

    def test_primary_retains_anti_affinity_for_replicas(self, helm, chart_path):
        """Verify primary still has podAntiAffinity to spread replicas across nodes."""
        deployment = self.helm_template_file(helm, chart_path, {}, "templates/statefulset-primary.yaml")

        pod_anti_affinity = findone(
            deployment,
            "spec.template.spec.affinity.podAntiAffinity",
        )

        assert pod_anti_affinity is not None, "Primary must retain podAntiAffinity to spread replicas"

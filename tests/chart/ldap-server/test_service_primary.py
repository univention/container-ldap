# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

from pytest_helm.utils import load_yaml

from univention.testing.helm.base import Base

POD_NAME = "statefulset.kubernetes.io/pod-name"


class TestServicePrimary(Base):
    template_file = "templates/service-primary.yaml"

    def get_selector(self, helm, chart_path, values):
        service = self.helm_template_file(helm, chart_path, values, self.template_file)
        return service.findone("spec.selector")

    def test_single_primary_is_selected_by_its_pod_name(self, helm, chart_path):
        selector = self.get_selector(helm, chart_path, {})

        assert selector[POD_NAME] == "release-name-ldap-server-primary-0"
        assert selector["ldap-server-type"] == "primary"

    def test_two_primaries_leave_the_pod_name_to_the_leader_elector(self, helm, chart_path):
        values = load_yaml(
            """
            replicaCountPrimary: 2
            """
        )

        selector = self.get_selector(helm, chart_path, values)

        assert selector[POD_NAME] == "will-be-updated-by-elector"

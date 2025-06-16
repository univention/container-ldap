# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest
from pytest_helm.utils import add_jsonpath_prefix, findone

from univention.testing.helm.base import Base


class TestStatefulsetResources(Base):
    container_name = "main"
    container_is_init = False

    def _get_resources(self, helm, chart_path, values, template_file):
        container_type = "initContainers" if self.container_is_init else "containers"

        deployment = self.helm_template_file(helm, chart_path, values, template_file)

        resources = findone(
            deployment,
            f"spec.template.spec.{container_type}[?@.name=='{self.container_name}'].resources",
        )
        return resources

    @pytest.mark.parametrize(
        "template_file",
        [
            "templates/statefulset-primary.yaml",
            "templates/statefulset-secondary.yaml",
        ],
    )
    def test_empty_resource(self, helm, chart_path, template_file):
        expected_resources = None

        values = {}

        resources = self._get_resources(helm, chart_path, values, template_file)

        assert resources == expected_resources

    @pytest.mark.parametrize(
        "template_file",
        [
            "templates/statefulset-primary.yaml",
            "templates/statefulset-secondary.yaml",
        ],
    )
    def test_resource(self, helm, chart_path, template_file):
        """
        Tests if the value for resourses would be set.
        """
        expected_resources = {
            "a": "resource-a",
            "b": "resource-b",
        }

        values = add_jsonpath_prefix(
            "resources",
            expected_resources,
        )

        resources = self._get_resources(helm, chart_path, values, template_file)

        assert resources == expected_resources

    @pytest.mark.parametrize(
        "template_file, value_path",
        [
            ("templates/statefulset-primary.yaml", "resourcesPrimary"),
            ("templates/statefulset-secondary.yaml", "resourcesSecondary"),
        ],
    )
    def test_overwritten_resource(self, helm, chart_path, template_file, value_path):
        """
        Tests if the value for resourses would be overwritten by resourcesPrimary/resourcesSecondary.
        """
        expected_resources = {
            "a": "resourceOverwritten-a",
            "b": "resourceOverwritten-b",
        }

        values = add_jsonpath_prefix(
            value_path,
            expected_resources,
        ) | add_jsonpath_prefix(
            "resources",
            {
                "a": "resource-a",
                "b": "resource-b",
            },
        )

        resources = self._get_resources(helm, chart_path, values, template_file)

        assert resources == expected_resources

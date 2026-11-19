# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import json
import re

import pytest

from univention.testing.helm.base import Base

FORCED_UCR_MOUNT = "volumeMounts[?@.mountPath=='/etc/univention/base-forced.conf']"
EXPORTER = "spec.template.spec.containers[?@.name=='slapd-exporter']"
PASSWORD_VOLUME = "spec.template.spec.volumes[?@.name=='metrics-bind-password']"

STATEFULSETS = ["templates/statefulset-primary.yaml", "templates/statefulset-secondary.yaml"]


@pytest.mark.parametrize("template_file", STATEFULSETS)
class TestMetricsSidecar(Base):
    def test_no_exporter_by_default(self, helm, chart_path, template_file):
        statefulset = self.helm_template_file(helm, chart_path, {}, template_file)

        assert statefulset.findall(EXPORTER) == []
        assert statefulset.findall(PASSWORD_VOLUME) == []

    def test_exporter_binds_as_the_ldap_admin(self, helm, chart_path, template_file):
        values = {
            "global": {"ldap": {"baseDn": "dc=stub,dc=test"}},
            "metrics": {"enabled": True},
        }
        statefulset = self.helm_template_file(helm, chart_path, values, template_file)

        args = statefulset.findone(EXPORTER)["args"]
        assert "--bind=simple" in args
        assert "--bind-dn=cn=admin,dc=stub,dc=test" in args

    def test_exporter_reads_the_password_from_the_existing_secret(self, helm, chart_path, template_file):
        values = {
            "metrics": {"enabled": True},
            "ldapServer": {
                "auth": {"existingSecret": {"name": "stub-secret", "keyMapping": {"password": "stub-key"}}},
            },
        }
        statefulset = self.helm_template_file(helm, chart_path, values, template_file)

        secret = statefulset.findone(PASSWORD_VOLUME)["secret"]
        assert secret["secretName"] == "stub-secret"
        assert secret["items"] == [{"key": "stub-key", "path": "password"}]

    def test_container_port_sets_listen_address_and_port(self, helm, chart_path, template_file):
        values = {"metrics": {"enabled": True, "containerPort": 9999}}
        statefulset = self.helm_template_file(helm, chart_path, values, template_file)

        exporter = statefulset.findone(EXPORTER)
        assert "--listen=:9999" in exporter["args"]
        assert exporter["ports"] == [{"name": "metrics", "containerPort": 9999, "protocol": "TCP"}]

    def test_main_mounts_forced_ucr_only_with_metrics(self, helm, chart_path, template_file):
        main = "spec.template.spec.containers[?@.name=='main']"
        default = self.helm_template_file(helm, chart_path, {}, template_file)
        enabled = self.helm_template_file(helm, chart_path, {"metrics": {"enabled": True}}, template_file)

        assert default.findone(main).findall(FORCED_UCR_MOUNT) == []
        assert enabled.findone(main).findone(FORCED_UCR_MOUNT)["subPath"] == "base-forced.conf"
        volume = enabled.findone("spec.template.spec.volumes[?@.name=='metrics-ucr-forced']")
        assert volume["configMap"]["name"] == "release-name-ldap-server-metrics-ucr"


class TestPodMonitor(Base):
    template_file = "templates/podmonitor.yaml"

    @pytest.mark.parametrize(
        "metrics",
        [
            {},
            {"enabled": True},
            {"podMonitor": {"enabled": True}},
        ],
    )
    def test_needs_metrics_and_pod_monitor_enabled(self, helm, chart_path, metrics):
        resources = helm.helm_template(chart_path, {"metrics": metrics})

        assert helm.get_resources(resources, kind="PodMonitor") == []

    def test_carries_the_configured_labels(self, helm, chart_path):
        values = {"metrics": {"enabled": True, "podMonitor": {"enabled": True, "labels": {"release": "stub"}}}}
        result = self.helm_template_file(helm, chart_path, values, self.template_file)

        assert result.findone("metadata.labels")["release"] == "stub"

    def test_scrapes_port_metrics_with_the_prometheus_defaults(self, helm, chart_path):
        values = {"metrics": {"enabled": True, "podMonitor": {"enabled": True}}}
        result = self.helm_template_file(helm, chart_path, values, self.template_file)

        endpoint = result.findone("spec.podMetricsEndpoints[0]")
        assert endpoint["port"] == "metrics"
        assert endpoint["path"] == "/metrics"
        assert "interval" not in endpoint
        assert "scrapeTimeout" not in endpoint

    def test_sets_interval_and_scrape_timeout(self, helm, chart_path):
        values = {
            "metrics": {
                "enabled": True,
                "podMonitor": {"enabled": True, "interval": "30s", "scrapeTimeout": "10s"},
            },
        }
        result = self.helm_template_file(helm, chart_path, values, self.template_file)

        endpoint = result.findone("spec.podMetricsEndpoints[0]")
        assert endpoint["interval"] == "30s"
        assert endpoint["scrapeTimeout"] == "10s"


class TestDashboardConfigMap(Base):
    template_file = "templates/configmap-metrics-dashboard.yaml"

    @pytest.mark.parametrize(
        "metrics",
        [
            {},
            {"enabled": True},
            {"dashboard": {"enabled": True}},
        ],
    )
    def test_needs_metrics_and_dashboard_enabled(self, helm, chart_path, metrics):
        resources = helm.helm_template(chart_path, {"metrics": metrics})

        assert helm.get_resources(resources, kind="ConfigMap", name="release-name-ldap-server-dashboard") == []

    def test_holds_the_ldap_server_dashboard(self, helm, chart_path):
        values = {"metrics": {"enabled": True, "dashboard": {"enabled": True}}}
        result = self.helm_template_file(helm, chart_path, values, self.template_file)

        dashboard = json.loads(result.findone("data")["nubus-ldap-server.json"])
        assert dashboard["uid"] == "nubus-ldap-server"


def dashboard_queries(node):
    """Yield every PromQL expression and variable query in a Grafana dashboard."""
    if isinstance(node, list):
        for item in node:
            yield from dashboard_queries(item)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key in ("expr", "query", "definition") and isinstance(value, str):
                yield value
            else:
                yield from dashboard_queries(value)


def selected_labels(query):
    """Return the label names a query filters, groups or lists by."""
    labels = set(re.findall(r"(\w+)\s*(?:=~|!~|!=|=)\s*\"", query))
    for grouping in re.findall(r"\b(?:by|without)\s*\(([^)]*)\)", query):
        labels.update(label.strip() for label in grouping.split(",") if label.strip())
    labels.update(re.findall(r"label_values\(.*,\s*(\w+)\)", query))
    return labels


# Labels the dashboard reads that the PodMonitor's relabelings do not set:
# Prometheus adds namespace and pod to every pod target, the exporter labels its series with suffix, op,
# direction and result, and kube-state-metrics labels its Lease series with lease and lease_holder.
LABELS_NOT_FROM_RELABELINGS = {"namespace", "pod", "suffix", "op", "direction", "result", "lease", "lease_holder"}


class TestDashboardMatchesPodMonitor(Base):
    values = {"metrics": {"enabled": True, "podMonitor": {"enabled": True}, "dashboard": {"enabled": True}}}

    @pytest.fixture
    def queries(self, helm, chart_path):
        configmap = self.helm_template_file(helm, chart_path, self.values, "templates/configmap-metrics-dashboard.yaml")
        return list(dashboard_queries(json.loads(configmap.findone("data")["nubus-ldap-server.json"])))

    @pytest.fixture
    def relabelings(self, helm, chart_path):
        pod_monitor = self.helm_template_file(helm, chart_path, self.values, "templates/podmonitor.yaml")
        return pod_monitor.findone("spec.podMetricsEndpoints[0].relabelings")

    def test_selects_the_job_the_pod_monitor_sets(self, queries, relabelings):
        job = next(relabeling["replacement"] for relabeling in relabelings if relabeling["targetLabel"] == "job")

        assert {name for query in queries for name in re.findall(r'job="([^"]*)"', query)} == {job}

    def test_selects_only_labels_the_pod_monitor_sets(self, queries, relabelings):
        set_by_relabelings = {relabeling["targetLabel"] for relabeling in relabelings}
        selected = set().union(*(selected_labels(query) for query in queries))

        assert selected - LABELS_NOT_FROM_RELABELINGS <= set_by_relabelings

    def test_reads_the_lease_of_the_leader_elector(self, helm, chart_path, queries):
        statefulset = self.helm_template_file(helm, chart_path, self.values, "templates/statefulset-primary.yaml")
        lease_name = statefulset.findone("spec.template.spec.containers[*].env[?@.name=='LEASE_NAME']")["value"]

        assert {name for query in queries for name in re.findall(r'lease="([^"]*)"', query)} == {lease_name}

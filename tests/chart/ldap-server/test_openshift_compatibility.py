# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

OPENSHIFT_API = ["--api-versions", "security.openshift.io/v1"]
FIXED_IDS = {"runAsUser", "runAsGroup", "fsGroup"}


def pod_specs(chart, helm_args=None):
    result = chart.helm_template(helm_args=helm_args)
    workloads = result.get_resources(kind="StatefulSet") + result.get_resources(kind="Deployment")
    assert workloads
    return [w.findone("spec.template.spec") for w in workloads]


def security_contexts(spec):
    yield spec.get("securityContext") or {}
    for container in spec.get("initContainers", []) + spec["containers"]:
        yield container.get("securityContext") or {}


def test_plain_kubernetes_keeps_fixed_ids(chart):
    assert any(FIXED_IDS & set(sc) for spec in pod_specs(chart) for sc in security_contexts(spec))


def test_openshift_removes_fixed_ids(chart):
    for spec in pod_specs(chart, helm_args=OPENSHIFT_API):
        for sc in security_contexts(spec):
            assert not FIXED_IDS & set(sc)

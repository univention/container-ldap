# Helm chart unit tests

This folder contains a set of unit tests which cover the behavior of the Helm chart.

These tests are based on `helm-test-harness` and `pytest-helm`.

See <https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm>
for further details about how to run the tests and how to develop new ones.

## TODOs

Since the `common-helm` version used for helm tests under `tests/chart` isn't compatible
anymore to the most current one, we use other tests under `helm-unittests` which may have
a high overlapping with the ones existing. But the newest one contains tests for the
templated keymapping.

This should be consolidated so that only one version is used in the future.
During implementation of [univention/dev/internal/team-nubus#1441](https://git.knut.univention.de/univention/dev/internal/team-nubus/-/issues/1441)
there wasn't enough time to do so.

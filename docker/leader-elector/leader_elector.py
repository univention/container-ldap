#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH
import logging
import signal
import sys
import time
from datetime import datetime, timedelta, timezone

from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    pod_namespace: str
    pod_name: str
    lease_name: str
    lease_duration_seconds: int
    retry_period_seconds: int
    renew_deadline_seconds: int


class LDAPLeaderElector:
    def __init__(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        self.core_api = client.CoreV1Api()
        self.coordination_api = client.CoordinationV1Api()
        self.settings = Settings()
        self.running = True
        signal.signal(signal.SIGINT, self.handle_sigint)
        self.is_currently_active = False
        self.is_currently_labeled_leader = False

    def handle_sigint(self, signum, frame):
        logger.info("Received SIGINT, releasing lease and exiting...")
        self.ensure_pod_is_hot_standby()  # Ensure we remove leader status
        self.release_lease()
        self.running = False
        sys.exit(0)

    def ensure_lease(self):
        """Ensure the lease exists"""
        try:
            self.coordination_api.read_namespaced_lease(
                name=self.settings.lease_name, namespace=self.settings.pod_namespace
            )
        except ApiException as e:
            if not e.status == 404:
                raise
            lease = client.V1Lease(
                metadata=client.V1ObjectMeta(name=self.settings.lease_name, namespace=self.settings.pod_namespace),
                spec=client.V1LeaseSpec(
                    holder_identity=self.settings.pod_name,
                    lease_duration_seconds=self.settings.lease_duration_seconds,
                    renew_time=None,
                ),
            )
            self.coordination_api.create_namespaced_lease(namespace=self.settings.pod_namespace, body=lease)

    def acquire_or_renew(self):
        """Acquire or renew the lease"""
        try:
            lease = self.coordination_api.read_namespaced_lease(
                name=self.settings.lease_name, namespace=self.settings.pod_namespace
            )
            current_time = datetime.now(timezone.utc)

            # If we're not the current holder, we can only acquire if the lease has expired
            if lease.spec.holder_identity != self.settings.pod_name:
                if lease.spec.renew_time is not None and current_time - lease.spec.renew_time.replace(
                    tzinfo=timezone.utc
                ) <= timedelta(seconds=self.settings.lease_duration_seconds):
                    # Lease is still valid and held by someone else
                    self.ensure_pod_is_hot_standby()
                    return False

            # Try to update the lease with our identity
            lease.spec.holder_identity = self.settings.pod_name
            lease.spec.renew_time = current_time.isoformat()

            self.coordination_api.replace_namespaced_lease(
                name=self.settings.lease_name, namespace=self.settings.pod_namespace, body=lease
            )
            return True
        except ApiException as e:
            logger.error(f"Failed to acquire/renew lease: {e}")
            return False

    def watch_lease(self):
        """Watch for lease changes"""
        w = watch.Watch()
        for event in w.stream(
            self.coordination_api.list_namespaced_lease,
            namespace=self.settings.pod_namespace,
            field_selector=f"metadata.name={self.settings.lease_name}",
        ):
            if not self.running:
                w.stop()
                return
            # Handle lease changes and attempt to acquire when appropriate
            self.handle_lease_event(event)

    def update_pod_leader_label(self, is_leader):
        """Update the pod's leader label for administrative visibility"""
        # Skip if no state change
        if is_leader == self.is_currently_labeled_leader:
            return

        try:
            label_value = "true" if is_leader else None
            self.core_api.patch_namespaced_pod(
                name=self.settings.pod_name,
                namespace=self.settings.pod_namespace,
                body={"metadata": {"labels": {"ldap-leader": label_value}}},
            )
            logger.info(f"Pod {self.settings.pod_name} {'labeled' if is_leader else 'unlabeled'} as leader")
            self.is_currently_labeled_leader = is_leader  # Update tracked state
        except ApiException as e:
            logger.error(f"Error updating pod leader label: {e}")

    def update_service_selector(self, make_active):
        """Update the service selector to point to this pod when it becomes the leader"""
        # Skip if no state change
        if make_active == self.is_currently_active:
            return

        try:
            service_name = f"{self.settings.pod_name.rsplit('-', 1)[0]}"
            body = {
                "spec": {
                    "selector": {"statefulset.kubernetes.io/pod-name": self.settings.pod_name if make_active else None}
                }
            }
            self.core_api.patch_namespaced_service(
                name=service_name, namespace=self.settings.pod_namespace, body=body, field_manager="leader-elector"
            )
            logger.info(f"Service selector {'updated to' if make_active else 'removed from'} {self.settings.pod_name}")
            self.is_currently_active = make_active  # Update tracked state
        except ApiException as e:
            logger.error(f"Error updating service selector: {e}")
            sys.exit(1)

    def ensure_pod_is_active_primary(self):
        """Configure pod as active primary"""
        self.update_pod_leader_label(True)
        self.update_service_selector(True)

    def ensure_pod_is_hot_standby(self):
        """Configure pod as hot standby"""
        self.update_pod_leader_label(False)
        self.update_service_selector(False)

    def release_lease(self):
        """Release the lease if we're the holder"""
        try:
            lease = self.coordination_api.read_namespaced_lease(
                name=self.settings.lease_name, namespace=self.settings.pod_namespace
            )
            if lease.spec.holder_identity == self.settings.pod_name:
                lease.spec.holder_identity = None
                lease.spec.renew_time = None
                self.coordination_api.replace_namespaced_lease(
                    name=self.settings.lease_name, namespace=self.settings.pod_namespace, body=lease
                )
                # Ensure we remove our pod from being the active primary
                self.ensure_pod_is_hot_standby()
        except ApiException:
            logger.error("Failed to release lease", exc_info=True)

    def run(self):
        """Main execution logic"""
        logger.info(f"Starting leader election for pod {self.settings.pod_name}")
        self.ensure_lease()

        while self.running:
            try:
                is_leader = self.acquire_or_renew()
                if is_leader:
                    self.ensure_pod_is_active_primary()
                else:
                    self.ensure_pod_is_hot_standby()
                    # Wait shorter time if we're not the leader
                    time.sleep(self.settings.retry_period_seconds)
                    continue

                # If we're leader, wait until near lease expiration before renewing
                time.sleep(self.settings.renew_deadline_seconds)

            except ApiException:
                logger.error("Failed to acquire/renew lease", exc_info=True)
                self.ensure_pod_is_hot_standby()
                time.sleep(self.settings.retry_period_seconds)


if __name__ == "__main__":
    try:
        elector = LDAPLeaderElector()
        elector.run()
    except Exception:
        logger.error("Fatal error in leader election", exc_info=True)
        sys.exit(1)

#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH
import logging
import os
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

    def handle_sigint(self, signum, frame):
        logger.info("Received SIGINT, releasing lease and exiting...")
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
        lease = self.coordination_api.read_namespaced_lease(
            name=self.settings.lease_name, namespace=self.settings.pod_namespace
        )
        current_time = datetime.now(timezone.utc)

        if (
            lease.spec.renew_time is None
            or lease.spec.holder_identity == self.settings.pod_name
            or (
                current_time - lease.spec.renew_time.replace(tzinfo=timezone.utc)
                > timedelta(seconds=self.settings.lease_duration_seconds)
            )
        ):
            lease.spec.holder_identity = self.settings.pod_name
            lease.spec.renew_time = current_time.isoformat()
            self.coordination_api.replace_namespaced_lease(
                name=self.settings.lease_name, namespace=self.settings.pod_namespace, body=lease
            )

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

    def ensure_pod_is_active_primary(self):
        """Configure pod as active primary"""
        self.update_pod_leader_label(True)
        with open("/var/run/lease/ldap-leader", "w") as f:
            f.write(self.settings.pod_name)

    def ensure_pod_is_hot_standby(self):
        """Configure pod as hot standby"""
        self.update_pod_leader_label(False)
        try:
            os.remove("/var/run/lease/ldap-leader")
        except FileNotFoundError:
            pass

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
        except ApiException:
            logger.error("Failed to release lease", exc_info=True)
            sys.exit(1)

    def run(self):
        """Main execution logic"""
        logger.info(f"Starting leader election for pod {self.settings.pod_name}")
        self.ensure_lease()

        while self.running:
            try:
                self.acquire_or_renew()
            except ApiException:
                logger.error("Failed to acquire/renew lease", exc_info=True)
                self.ensure_pod_is_hot_standby()
                self.watch_lease()
            else:
                self.ensure_pod_is_active_primary()
                time.sleep(self.settings.renew_deadline_seconds)


if __name__ == "__main__":
    try:
        elector = LDAPLeaderElector()
        elector.run()
    except Exception:
        logger.error("Fatal error in leader election", exc_info=True)
        sys.exit(1)

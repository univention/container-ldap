#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import os
import time
from datetime import datetime, timedelta, timezone

from kubernetes import client, config
from kubernetes.client.rest import ApiException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LDAPLeaderElector:
    def __init__(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

        self.core_api = client.CoreV1Api()
        self.coordination_api = client.CoordinationV1Api()
        self.namespace = os.getenv("POD_NAMESPACE")
        self.pod_name = os.getenv("POD_NAME")
        self.lease_name = os.getenv("LEASE_NAME", "ldap-primary-leader")
        self.lease_duration = int(os.getenv("LEASE_DURATION_SECONDS", "15"))
        self.retry_period = int(os.getenv("RETRY_PERIOD_SECONDS", "5"))
        self.renew_deadline = int(os.getenv("RENEW_DEADLINE_SECONDS", "10"))

    def create_lease(self):
        """Create the lease if it doesn't exist"""
        try:
            self.coordination_api.read_namespaced_lease(name=self.lease_name, namespace=self.namespace)
        except ApiException as e:
            if e.status == 404:
                # Lease doesn't exist, create it
                lease = client.V1Lease(
                    metadata=client.V1ObjectMeta(name=self.lease_name, namespace=self.namespace),
                    spec=client.V1LeaseSpec(
                        holder_identity=self.pod_name, lease_duration_seconds=self.lease_duration, renew_time=None
                    ),
                )
                self.coordination_api.create_namespaced_lease(namespace=self.namespace, body=lease)
            else:
                raise

    def try_acquire_or_renew(self):
        """Try to acquire or renew the lease"""
        try:
            lease = self.coordination_api.read_namespaced_lease(name=self.lease_name, namespace=self.namespace)
            current_time = datetime.now(timezone.utc)

            # Check if lease is expired or we are the holder
            if (
                lease.spec.renew_time is None
                or lease.spec.holder_identity == self.pod_name
                or (
                    current_time - lease.spec.renew_time.replace(tzinfo=timezone.utc)
                    > timedelta(seconds=self.lease_duration)
                )
            ):
                # Update lease with our identity
                lease.spec.holder_identity = self.pod_name
                # Convert to ISO format string
                lease.spec.renew_time = current_time.isoformat()
                self.coordination_api.replace_namespaced_lease(
                    name=self.lease_name, namespace=self.namespace, body=lease
                )
                return True
            return False
        except ApiException as e:
            logger.error(f"Error while trying to acquire/renew lease: {e}")
            return False

    def update_pod_leader_label(self, is_leader):
        try:
            label_value = "true" if is_leader else None
            self.core_api.patch_namespaced_pod(
                name=self.pod_name,
                namespace=self.namespace,
                body={"metadata": {"labels": {"ldap-leader": label_value}}},
            )
            logger.info(f"Pod {self.pod_name} {'labeled' if is_leader else 'unlabeled'} as leader")
        except ApiException as e:
            logger.error(f"Error {'labeling' if is_leader else 'unlabeling'} pod as leader: {e}")

    def run(self):
        """Main loop for leader election"""
        logger.info(f"Starting leader election for pod {self.pod_name}")
        self.create_lease()

        while True:
            try:
                is_leader = self.try_acquire_or_renew()
                self.update_pod_leader_label(is_leader)

                if is_leader:
                    logger.info(f"Pod {self.pod_name} is the leader")
                    with open("/var/run/lease/ldap-leader", "w") as f:
                        f.write(self.pod_name)
                else:
                    logger.info(f"Pod {self.pod_name} is not the leader")
                    try:
                        os.remove("/var/run/lease/ldap-leader")
                    except FileNotFoundError:
                        pass

                time.sleep(self.retry_period)
            except Exception as e:
                logger.error(f"Unexpected error in leader election loop: {e}")
                time.sleep(self.retry_period)


if __name__ == "__main__":
    elector = LDAPLeaderElector()
    elector.run()

# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH
from functools import lru_cache

from pydantic_settings import BaseSettings


class LDIFProducerSettings(BaseSettings):
    # Nats user name specific to UdmProducerSettings
    nats_user: str
    # Nats password specific to UdmProducerSettings
    nats_password: str
    # Nats: host
    nats_host: str
    # Nats: port
    nats_port: int
    nats_max_reconnect_attempts: int

    # File location for the unix socket to the ldap server
    socket_file_location: str
    # Maximum number of messages that are buffered and waiting to be sent to NATS
    max_in_flight_ldap_messages: int
    # Number of concurrent LDAP threads.
    ldap_threads: int
    # Base DN of the LDAP tree
    ldap_base_dn: str
    # Configure whether to ignore temporary ldap objects, e.g. Lock objects created by UDM.
    ignore_temporary_objects: bool

    @property
    def nats_server(self) -> str:
        return f"nats://{self.nats_host}:{self.nats_port}"


@lru_cache
def get_ldif_producer_settings() -> LDIFProducerSettings:
    return LDIFProducerSettings()

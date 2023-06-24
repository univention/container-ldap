# Bundling of portal extensions

---

- date: 2023-06-24
- deciders:
  - johannes.bornhold.extern@univention.de

---

## Context

The container `ldap-server` needs extensions from various other applications to
be applied, so that they can be successfully integrated with the containerized
OpenLDAP.

Currently all needed extensions are added directly into the container image
during build time. A solution to allow dynamic extensions is under discussion
and may replace this solution in the future.

The extensions are typically part of the respective Debian package. During the
work on the containerization of the Univention Management Stack a solution for a
Continuous Integration between the work on the portal and the work on the ldap
container is needed. A solution for handling Debian packages in this process is
not yet found.


## Decision

The needed extensions from the portal are packaged as a container image.


## Consequences

The integration between the work on the portal and the ldap container can be
integrated based on the well understood path for container images.

Potentially added value from the Debian package manager cannot be used in this
path.

A future refactoring is needed once the handling of versions, the release flow
and also the packaging details have been worked out and stabilized sufficiently.


## Considered alternative options

Using the registry for generic packages of Gitlab would have been an alternative
option to hand the Debian package from the portal project to the ldap container
project in Gitlab. In comparison to the use of container images this approach
looked more complicated and more difficult to use locally.

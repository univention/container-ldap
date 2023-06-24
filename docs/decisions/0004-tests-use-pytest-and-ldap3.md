# Using `pytest` and `ldap3` for the testsuite

---

- date: 2023-06-24
- deciders:
  - johannes.bornhold.extern@univention.de

---


## Context

A simple way to interact with the container `ldap-server` is needed to verify if
certain object types can be added into the OpenLDAP server.


## Decision

The new tests will be based on the test runner `pytest` and use `ldap3` for the
LDAP interaction.


## Consequences

Test cases can be implemented as plain Python functions without the overhead of
an abstraction to describe desired behavior.

The testing dependencies are simplified because `ldap3` is built in pure Python,
this does simplify setting up dependencies locally. An ORM abstraction is
available which eases interaction with the LDAP objects.

The existing integration tests will at some point in the future need a migration.

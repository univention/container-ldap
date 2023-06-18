# Architectural Decision Records (ADRs)

---

- status: accepted
- date: 2023-06-18
- deciders:
  - johannes.bornhold.extern@univention.de

---

## Context

Relevant design decisions regarding the implementation of the ldap container are
not available in the source code repository. Developers who work on this in the
future may have no way to discover those decisions and their rationale again,
thus repeating part of the required learning loop.

We are now updating the container implementation to assemble a purely container
based stack to provide the same functionality which the appliance based setup
does provide. This does mean that we are about to make further relevant
decisions.


## Decision

Relevant decisions will be logged as Lightweight Architecture Decision Records
(ADRs) within the repository as part of the documentation in the folder
`./docs/decisions`.


## Consequences

Relevant decisions are available together with the source code. This will allow
future colleagues to better understand the design and to be more productive and
successful when working with this codebase.


## More information

### Background

https://adr.github.io/

### Example ADR

The strucure of MADR 3.0.0 https://adr.github.io/madr/#example is used.

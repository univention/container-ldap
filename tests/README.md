# Test Organization


## TL;DR run the tests

```
# Use "pipenv" to have the right environment
pipenv sync -d
pipenv run pytest

# Get a shell
pipenv shell
```


## Target structure

The target structure for testing shall eventually follow this pattern:

```
└── tests  # top-level tests folder
    ├── README.md  # explains test organization inside this folder
    ├── unit  # name this unit_and_integration if keeping both here
    ├── integration  # optional: omit if kept together with unit tests
    └── e2e
```

### Unit tests

The *unit* under test is in this repository the "container":

- `ldap-server` is the OpenLDAP server

- `ldap-notifier` is the Univention Directory Notifier

Simple checks which focus on a single container are kept in the subdirectory
`unit`.


### Integration tests

The current integration tests are in the folder `integration-test` in the root
of this repository. The aim is to migrate those eventually into the folder
`integration` as shown above in the overview.

Tests which check the *integration* of multiple containers will be grouped into
the folder `integration` as shown above in the overview.

New tests are written as plain `pytest` based test cases.


### End to end tests

This repository contains no end-to-end tests. *End to end* is understood as
tests against the full running stack, so they are expected to be kept
separately.

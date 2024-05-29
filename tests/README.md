# Test Organization

## TL;DR run the tests

In a container:

```shell
docker compose up --build test
```

Locally:

```sh
poetry install
poetry shell
pytest --cov=univention/provisioning/ --cov-report term-missing -v
```

## Target structure

The target structure for testing shall eventually follow this pattern:

```
└── tests
    ├── README.md
    ├── unit
    ├── integration
    └── e2e
```

### Unit tests

Unit tests can run without any external dependencies.

The unittests in this repository test the python code
of the the LDIF-Producer slapd-socket server.

the LDIF-Producer is a multithreaded application
using the python threading library.
Due to this fact, some unittests take around a second to execute
or more explicitly to shut down
because the exit signal can only be evaluated
between polling intervals.

The multithreaded nature of the LDIF-Producer
makes debugging test failures significantly harder.
Tests can seem to be "hanging forever"
when a worker thread throws an exception.

The LDIF-Producer implements extensive logging to help in debugging.
In a pytest run, you can activate the logs with the `-s` and `--full-trace`
cli arguments.

As a last resort, you can separate `stdout` from `stderr`
you can sort the logs by process id to reveal different patterns.

```sh
docker logs dev-local-ldif-producer-1 > ldif-producer.log \
&& docker logs dev-local-ldif-producer-1 2>> ldif-producer.log \
&& vim ldif-producer.log
```

vim sort command:
`:sort /\[\d \d*\]/`

### Integration tests

Integration tests are all test that depend on separately started containers.
Those can be the `ldap-server`, `ldif-producer` and `nats`.
Integration tests may need only one, some or all of those containers

the tests in the `integration-tests` folder are assumed to be deprecated.

### End to end tests

This repository contains no end-to-end tests. *End to end* is understood as
tests against the full running stack, so they are expected to be kept
separately.

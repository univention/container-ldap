===========
 Changelog
===========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


`Unreleased`_
=============


Added
-----

- Add the Univention Portal related schema extensions from the release artifact
  `portal-udm-extensions` to ensure that the latest adjustments are included.
  This is an interim solution which will evolve in the future.

- Add documentation based on Sphinx docs with the default Univention templates.

- Add Helm charts to allow the installation of the `ldap-server` and the
  `ldap-notifier` into a given Kubernetes cluster.

- Extend the docker compose configuration so that an instance of phpLDAPadmin is
  running. This provides a simple way to inspect and interact with the OpenLDAP
  server.


Changed
-------

- Configure the initial admin password in plain text instead of having to
  provide a hashed value.

- Update the Dockerfile per container and the Gitlab CI configuration, so that
  the images can be built again both locally and in the CI/CD pipeline.

- The volume configuration for the setup based on docker compose has been
  simplified, so that one persistent volume is used for data persistency and for
  the collaboration between OpenLDAP and the Notifier server.

  The Helm chart does reflect the same volume configuration.


Removed
-------

- Removed the Python based implementation of the CI/CD pipeline jobs. The
  configuration is now relying on plain features of Gitlab's CI. It is also
  leveraging `common-ci`.







.. _unreleased: https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/-/commits/main?ref_type=heads

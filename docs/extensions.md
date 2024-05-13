
Schema Extensions (UDM Extensions)
==================================

The Univention Directory Manager (UDM) does support extensions which also can
include LDAP related extensions:

- Schema extensions

- ACL extensions

If everything is installed on a traditional machine, then the installation via
the package manager can trigger the needed adjustments in the configuration for
the LDAP server.

In a container based deployment the image itself is considered as an immutable
artifact, the concept of plugging in extensions at runtime does not fit
directly.

The currently included extensions can be inspected in the file
`docker/ldap/Dockerfile`.

Further details regarding the UDM are available at the following URL:
https://docs.software-univention.de/developer-reference/5.0/en/udm/index.html


Extension handling for containers
=================================

There is no support to add extensions after the container image has been built.
All extensions which shall be used have to be integrated into the image during
build time.

The integration process is implemented in the following two steps which are in a
multi stage Dockerfile:

1. A builder image is used to install the various Debian packages which contain
   relevant extensions.

2. The target image is then built by taking only the schema extensions out of
   the builder image, so that the remaining parts of the installed packages are
   not leading to a bloated result.

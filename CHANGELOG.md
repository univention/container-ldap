# Changelog

## [0.8.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.8.1...v0.8.2) (2023-12-21)


### Bug Fixes

* **licensing/ci:** add spdx license headers, add license header checking with common-ci v1.13.x ([dbb3a94](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/dbb3a94b444f3f7806f529a2669aac0f057bdcab))

## [0.8.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.8.0...v0.8.1) (2023-12-21)


### Bug Fixes

* **docker:** update ucs-base from 5.0-5 to 5.0-6 ([f2f15c4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f2f15c4c9fb3be6c95ad80104faa51d6a842ecfa))

## [0.8.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.7.2...v0.8.0) (2023-12-20)


### Features

* **server:** add guardian schema ([8728238](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/8728238d1c4985cbaf3f3e661e3a265f2465ee4d)), closes [univention/customers/dataport/team-souvap#342](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/342)

## [0.7.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.7.1...v0.7.2) (2023-12-18)


### Bug Fixes

* **ci:** add Helm chart signing and publishing to souvap via OCI ([a8a452f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a8a452f064529850d78138973b0a7be12460363a))

## [0.7.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.7.0...v0.7.1) (2023-12-11)


### Bug Fixes

* **ci:** reference common-ci v1.11.0 to push sbom and signature to souvap ([a0f1077](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a0f10774d5ecebab8d3a81999e9a05f65bca90f5))

## [0.7.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.6.0...v0.7.0) (2023-11-15)


### Features

* **server:** add ACL for self-service ([7e42e66](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/7e42e666b4fab49c33f0b887db3c2c8fc4fe212f))

## [0.6.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.5.3...v0.6.0) (2023-11-14)


### Features

* **helm:** support for extra volumes ([50ddd93](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/50ddd937bd39221ec93a39429a59ee33fb8cac78))

## [0.5.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.5.2...v0.5.3) (2023-11-14)


### Bug Fixes

* Add "kerberos/realm" in UCR values for test run ([3543a0f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3543a0f1e8f582d3898c70e01b2cc095dd479eca))

## [0.5.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.5.1...v0.5.2) (2023-11-13)


### Bug Fixes

* Pin the version of portal-udm-extensions ([d830557](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d830557352bca09beada76a96a223e831a302513))

## [0.5.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.5.0...v0.5.1) (2023-11-13)


### Bug Fixes

* **ldap-server:** Ensure that notifier directories exist ([2012d36](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2012d36d7da8006523d0d4aa8dcc7c408428845d))

## [0.5.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.4.3...v0.5.0) (2023-11-10)


### Features

* Remove custom deb builder container ([f61ab66](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f61ab6661fa7feee2020b7c30bd748bd1085d8e6))
* Use the plain univention ldap packages ([cb1df95](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/cb1df951776ab19897680ebd362aa9981648dd62))

## [0.4.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.4.2...v0.4.3) (2023-11-10)


### Bug Fixes

* **helm:** add a toggle to enable the wait-for-SAML init container ([ee91fb4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ee91fb4c20adde48672a5849df9507af4a8bc291))

## [0.4.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.4.1...v0.4.2) (2023-11-09)


### Bug Fixes

* **server:** read UCR settings from ConfigMap ([1d6270b](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1d6270b3eca5385e7bb6b9a05b72090486b465a2))
* **tests:** run tests using DinD instead of GitLab services ([566fc2d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/566fc2db3f6a6ce6e32fd4d366d67d7afac31a7f))

## [0.4.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.4.0...v0.4.1) (2023-11-06)


### Bug Fixes

* **docker:** bump common-ci to build latest image ([6710b8b](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/6710b8bec8586639b37fa221ec077cf6c5049495))

## [0.4.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.3.1...v0.4.0) (2023-11-03)


### Features

* **helm:** The Pod "ldap-server" waits until the SAML metadata is available ([eb3f6c9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/eb3f6c9f7736ff1b136b538e081acc144661c00f))

## [0.3.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.3.0...v0.3.1) (2023-11-03)


### Bug Fixes

* **versions:** produce version-tagged Docker images ([f8b8b02](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f8b8b02a20966f5186c76490e461b6753ffaaae5))

## [0.3.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.2.0...v0.3.0) (2023-11-02)


### Features

* **server:** ox-connector schemas ([f62a762](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f62a762b0ec46db3a482eb2b6d40661ee2362614))

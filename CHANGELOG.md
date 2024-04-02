# Changelog

## [0.10.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.10.2...v0.10.3) (2024-04-02)


### Bug Fixes

* pinning container name to ldap-notifier ([35cb66c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/35cb66c8e5e73b86cd574340fa55e2584aa7534d))

## [0.10.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.10.1...v0.10.2) (2024-03-25)


### Bug Fixes

* **ci:** update common-ci from v1.24.4 to v1.24.5 ([8406404](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/840640408159f8d7d14af37d6d3b54d3d56c021b))

## [0.10.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.10.0...v0.10.1) (2024-03-21)


### Bug Fixes

* create communication files with permissions of the ldap server ([9c9d4b9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9c9d4b9aaba58577d523a2256d1cd6b19dec0792))

## [0.10.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.9.5...v0.10.0) (2024-03-20)


### Features

* **Helm/container:** BSI-compliant bitnami based Helm chart ([56f4c24](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/56f4c2420ac3915672b94d6ca05ffaaec7a5c9c3))


### Bug Fixes

* add mising ucr entries ([bcb20e8](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bcb20e804b55a8835aa633025463e33a53506c40))
* adding devops-based helm chart, making required adjustment to entrypoint script ([9c6ae9d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9c6ae9d4a3b6126c75a56861c1fad651a13a5864))
* adjust ldap-notifier registry ref ([d35befc](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d35befcc94bcb39ec42fcd4e756f2d7af5da4595))
* make resources for init containers adjustable via values ([78db204](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/78db2044754b0045b1f689f9c49d43e3a1628d77))
* re-add waitForDependency ([ceca47e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ceca47e7363cff4921b8063ad73e8f2d005c609b))
* remove duplicates from base-defaults.conf ([0331ad4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/0331ad4d04b4440dd5391bc13e74fffee0a8f081))
* remove unwanted chart category ([a10b7d0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a10b7d05e0629d45d7372af150a6e303da6f5d4a))
* update common-ci ref ([8ace7bd](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/8ace7bd95b93ee711fb7ef8cd6035f8ba86cbd51))

## [0.9.5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.9.4...v0.9.5) (2024-03-19)


### Bug Fixes

* Update TLS related UCR variables to "directory/manager/starttls" ([72d4b86](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/72d4b8664f341a36ac2506aff085b902871268f6))

## [0.9.4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.9.3...v0.9.4) (2024-03-19)


### Bug Fixes

* Remove "appVersion" from chart "ldap-server" ([473c474](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/473c474a30f835b5697fd6c14947128e402a1f98))

## [0.9.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.9.2...v0.9.3) (2024-03-12)


### Bug Fixes

* add get_int to ucr-light-filter Registry implementation ([2de4ea3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2de4ea32cb20d468ae16a98e2ec2791df9c1b967))
* restore upstream ucr compatibility ([1306b86](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1306b867ee453fef59dac8249370e711e4cb9ba5))

## [0.9.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.9.1...v0.9.2) (2024-01-31)


### Bug Fixes

* **deps:** update all dependencies ([57b8d3f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/57b8d3f83e0af84b24420170937f4d016aae0e5b))

## [0.9.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.9.0...v0.9.1) (2024-01-23)


### Bug Fixes

* **helm:** Use the internal knut registry as default image source ([b328966](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/b32896634b007d11082231582f6c24594609ae42))

## [0.9.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.8.2...v0.9.0) (2024-01-16)


### Features

* **ci:** add debian update check jobs for scheduled pipeline ([232ec97](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/232ec97bb62143aa61a7d6d9b1dda35502f14587))


### Bug Fixes

* **deps:** add renovate.json ([78b12eb](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/78b12eb3004c8946a785eaff6fd81a8434d56e4c))

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

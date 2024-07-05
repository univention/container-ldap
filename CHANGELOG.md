# Changelog

## [0.20.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.20.0...v0.20.1) (2024-07-05)


### Bug Fixes

* update base to UCS 5.2 ([e27c2e5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e27c2e5c0bc469998c53983c352dc53f455c9ec3))

## [0.20.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.19.0...v0.20.0) (2024-07-05)


### Features

* Add support for dynamic extension configuration ([cc8d63c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/cc8d63c23f98be5b0133e62e28500af7c85abcb6))

## [0.19.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.18.1...v0.19.0) (2024-07-04)


### Features

* remove extensions for Guardian, App Center; keep Self-service; temp. keep Portal, OX-Connector ([fccd26e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fccd26e33faf154a862f9471dab64ac5b088b45a))

## [0.18.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.18.0...v0.18.1) (2024-07-04)


### Bug Fixes

* **ldif-producer:** copy SlapdSockHandler.handle() into subclass ([d656aa7](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d656aa72a56a29e3da0181cb7d5d321493d505ff))
* **ldif-producer:** don't cache handler function responses ([f512e4d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f512e4dfd8630114dd3b81630c0bb4c1ab60486c))
* **ldif-producer:** ignore memberOf overlay requests in do_result aswell ([b575dfd](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/b575dfd492a556071e696b3fe872e60bcbe3c52f))
* **ldif-producer:** ignore socket requests from the memeberOf overlay and add test-cases for it ([876975c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/876975ca2564a855fe182743d8186734a2692bf5))
* **ldif-producer:** improve tests and raise exceptions in unittest scenarios ([b208d18](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/b208d18b8fed82f7d05f99b58bd0f0f95d594fa9))
* **ldif-producer:** improvements with Arvid ([068419f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/068419fba210429546cbb0228128699872547554))
* **ldif-producer:** LDAPHandler unit tests ([4ae3214](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/4ae3214b85d13ffa5751ee46e6f7ff160fbafb51))
* **ldif-producer:** make backpressure timeout configurable ([66a64f6](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/66a64f6777084cb3aa031ece280c09d3955f1609))
* **ldif-producer:** optionally ignore temporary objects also in pre-hooks ([0930ec7](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/0930ec762855cd09c7e01cad224238452025e116))

## [0.18.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.17.1...v0.18.0) (2024-06-27)


### Features

* Update the ox-connector extensions to version 0.9.0 ([f3d3ab8](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f3d3ab850aa61b7b1a18ed80ceead93179702b06))

## [0.17.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.17.0...v0.17.1) (2024-06-25)


### Bug Fixes

* bump ucs-base to 5.0-8 ([f37579d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f37579d40684c2c33399ed35ac396f99f15218c5))

## [0.17.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.16.0...v0.17.0) (2024-06-19)


### Features

* Adjust build to updated portal-extension image (former portal-udm-extensions) ([74dce4c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/74dce4c34a137f34adc1715bb7f41045773842dd))
* Update the portal-extensions version to 0.26.0 ([d846f20](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d846f20523936045c6bf93092061edbd19de4d8d))

## [0.16.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.15.2...v0.16.0) (2024-06-14)


### Features

* **ldap-server:** install and activate lapdsock in the ldap-server container ([1ca787d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1ca787de6ed9c92780ad00c9494d1454b280abcc))
* **ldif-producer:** scaffolding to push messages to nats ([e355f6e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e355f6ea28270b57ee1c288bf59a230f0bb5da0e))
* **ldif-producer:** separate asyncio thread ([03d0e31](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/03d0e318e564da9397110013219f121da303ea63))
* **ldif-producer:** wip docker-compose ([12df461](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/12df461d46c312075f424e67a0d2e656252740aa))


### Bug Fixes

* **ldif-producer:** add exit signal handling ([39729ac](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/39729ac53e1306cb8f6be1cff247cd9b56e1188d))
* **ldif-producer:** add nats to docker-compose ([dd57f1a](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/dd57f1a7715e6d1607a92cd19de577e448335b7e))
* **ldif-producer:** Adjust slapd-sock path ([2db3d80](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2db3d805aa6a16ec42134ac90cff63fe2ca58df3))
* **ldif-producer:** better logging for threaded app ([bf0ce63](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bf0ce63ef150bd776dbe148338368dc12a3600f0))
* **ldif-producer:** copy demo files from Arvid ([90f2a99](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/90f2a99b716ef15d69db75949470bfe05dd6a147))
* **ldif-producer:** increase backpressure timeout ([e392799](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e3927998663f33e906b5ebe5def95cab8992788f))
* **ldif-producer:** refinements with arvid ([3592a5f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3592a5fc1a11871f230ba5167297efbd8ed421e1))
* **ldif-producer:** some cleanup ([3bf12ea](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3bf12eacca471bef10f8c7df85d2fb2dbe051e3b))
* **ldif-producer:** sort-of working SlapdSockServer ([42b59ec](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/42b59ec92ea91313929488f357c900179deca9fa))
* **ldif-producer:** update dependencies and project metadata ([942cef1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/942cef151f65367d5a9246fab25ea0a343cb8547))

## [0.15.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.15.1...v0.15.2) (2024-05-24)


### Bug Fixes

* **ci:** use fixed common-ci/helm package to not update dependency waiter tags ([a2e9e80](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a2e9e80b2de1c0bee9b73a29f123b2327f34ac51))

## [0.15.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.15.0...v0.15.1) (2024-05-23)


### Bug Fixes

* ldap-notifier use global registry ([435be6e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/435be6e259da6e061fdd424bea621760ba1c5f5a))

## [0.15.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.14.0...v0.15.0) (2024-05-23)


### Features

* push to harbor ([ff9fe15](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ff9fe151d9d57b94bde722c93436a613750208e2))

## [0.14.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.13.0...v0.14.0) (2024-05-21)


### Features

* add back_ldap proxy configuration ([0569ccf](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/0569ccf727f7ba93e14339d42e5d0a1537002be0))
* allow for separate podAnnotations for primaries, secondaries and proxies ([e990b65](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e990b65369caa44b1d6f571fd053d8ed1d201b2b))
* allow for simplified HA configuration ([3ce1263](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3ce12639a4c3690af77edcc3234fee90a01ca57c))
* make primary a scalable multi-master configuration ([156c8b0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/156c8b00be046440bef9579227f47365df10f65a))
* split into primary and secondary instances, secondary instances scalable ([026c0d9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/026c0d98e6405c1e8bda97d3c09153d3334b899a))
* support for templating of global.configMapUcr ([f48733f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f48733f18e50e98c61f2994831348f57587ee679))
* type based replicacounts and resource specification, pre-flight check, service selector based on replicacounts ([00b530a](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/00b530a23a7e48e7ea99620cec09acb17a396cd5))


### Bug Fixes

* add LOG_LEVEL variable definition to entrypoint script ([290214d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/290214de0e95fded5a8500f245fb91c1a8db81e3))
* add sasl proxy authentication support ([85065a1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/85065a1c35509713bc1e64c6ca1612177808d915))
* fine-tuning network values for syncrepl ([4718fad](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/4718fad8291a2fa9a1cb2af6f963c97a7520c8c8))
* pod affinities and antiaffinities ([9b9c27d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9b9c27ddcef4e9e2d64411fa7bd7d3913b09e28e))

## [0.13.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.12.0...v0.13.0) (2024-05-07)


### Features

* Update base image to 5.0-7 ([689b4b6](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/689b4b6f68e42f4b3db2d792c558ea7c8b5b1d8c))

## [0.12.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.11.0...v0.12.0) (2024-04-25)


### Features

* changes to support the refactored umbrella values in a nubus deployment ([04d3337](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/04d33379e77afe010cbefc970678be6080646b86))
* export nubusTemplates.ldapNotifier.connection.host ([ad24c75](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ad24c75a65b813a416d28c88f93b6679f9bf73ab))
* set additional nubusTemplates ([b2cb030](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/b2cb03069e016adaff58a4454faf9fe4cb707b09))


### Bug Fixes

* configMapForced default value, only use global values for baseDn and domainName, added adminDn template, set waitForDependency tag to latest ([61dc87f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/61dc87fae5fe1e2d2419fb36c4193a8e8bd38687))
* typos, change samlMetadataUrl and samlMetadataUrlInternal to http protocol ([859a6ce](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/859a6cef26e679236b0eeb8a14025d6cc864aafd))

## [0.11.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.10.3...v0.11.0) (2024-04-19)


### Features

* Avoid call to "apt-get update" in builder stage ([cf10ee9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/cf10ee94749825d9b5d4c8de9f2316c8c03a93c1))
* Avoid calling "apt-get update" in final stage of ldap-server ([844547f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/844547f3826ead77947b86918d6bad71e6dab5df))
* Use date based build tag of the base image in ldap-notifier ([1c1e090](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1c1e090b91382999017b9225ba5a0abd9bfbd5f4))
* Use the date tagged base image to ensure a stable base package set ([2227da1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2227da179ffb185bf97943801d8cd3635a0d4883))

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

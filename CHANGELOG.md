# Changelog

## [0.47.6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.47.5...v0.47.6) (2025-11-21)


### Bug Fixes

* bump images in the values ([24a7d7b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/24a7d7b026b55947625875d6496189ad446b7d05)), closes [univention/dev/internal/team-nubus#1476](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1476)

## [0.47.5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.47.4...v0.47.5) (2025-11-05)


### Bug Fixes

* **ldap-notifier:** Adapt apt usage to be in line with base image ([33edd7f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/33edd7f3bc290627ae5ba8cc28f177fbcd79ae58)), closes [univention/dev/internal/team-nubus#1486](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1486)
* **ldap-notifier:** Install libunivention-config0 ([3e0f531](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/3e0f5319db0e8ff9db3283c8ee39ed87d8a9e3f0)), closes [univention/dev/internal/team-nubus#1486](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1486)

## [0.47.4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.47.3...v0.47.4) (2025-11-04)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20251030 ([2ee89a3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/2ee89a37ad64e79b50e8131e2fb83e016a0ea658)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)

## [0.47.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.47.2...v0.47.3) (2025-10-17)


### Bug Fixes

* make all helm tests pass with helm test version >=0.27.0 ([268b61d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/268b61dd4082bffaaba9e69989646a44bec9c32d)), closes [univention/dev/internal/team-nubus#1441](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1441)

## [0.47.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.47.1...v0.47.2) (2025-10-08)


### Bug Fixes

* **ldap-server:** Remove unused domain name ([3d1b893](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/3d1b893a6f5523c2c66db4d2117b9aa686aabb05)), closes [univention/dev/internal/team-nubus#1425](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1425)

## [0.47.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.47.0...v0.47.1) (2025-09-29)


### Bug Fixes

* Automated kyverno tests ([a220a79](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/a220a796d22fbe0d8a8fbe489064e21a4ce076bf)), closes [univention/dev/internal/team-nubus#1426](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1426)

## [0.47.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.46.3...v0.47.0) (2025-09-12)


### Features

* **ldap-server:** support LDAP bind via SASL OAUTHBEARER ([0cd94e7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/0cd94e71713cc5673e0bf58f6f019416debed59e)), closes [univention/dev/internal/dev-issues/dev-incidents#138](https://git.knut.univention.de/univention/dev/internal/dev-issues/dev-incidents/issues/138)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/testrunner Docker tag to v0.24.3 ([17d7cfb](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/17d7cfb89bff714f20530d6fe9d4544c535e7ce2)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)
* **ucr-light-filter:** fix handling of UCRWARNING ([b11ead3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/b11ead36e74d66b91949c46dab7919f5f173d40e)), closes [univention/dev/internal/dev-issues/dev-incidents#138](https://git.knut.univention.de/univention/dev/internal/dev-issues/dev-incidents/issues/138)

## [0.46.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.46.2...v0.46.3) (2025-09-02)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250828 ([1fc5305](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/1fc5305f075bbd8373091233f75be4d1ab716ba0)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)

## [0.46.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.46.1...v0.46.2) (2025-08-28)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.2 ([bb28507](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/bb28507b26d5178fc60a47c56fd93cd3b34ecefb)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)

## [0.46.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.46.0...v0.46.1) (2025-08-27)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250821 ([6e5d96e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/6e5d96e8819b578e3f183af7d627941ca7803ea2)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)

## [0.46.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.45.0...v0.46.0) (2025-07-25)


### Features

* Allow more than 10 ldap secondaries ([51eb28d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/51eb28d80b187631248c8f7a3368ca8ab489d869)), closes [univention/dev/internal/team-nubus#1353](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1353)

## [0.45.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.44.0...v0.45.0) (2025-07-17)


### Features

* update wait-for-dependency to 0.35.0 ([d92622c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/d92622c8e250578f985758aa1195ef59b8ed4cf6)), closes [univention/dev/internal/team-nubus#1320](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1320)

## [0.44.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.43.0...v0.44.0) (2025-07-17)


### Features

* update ucs-base to 5.2.2-build.20250714 ([62c2e32](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/62c2e32a056064e3d68dcf8c893fea8e2746eb6a)), closes [univention/dev/internal/team-nubus#1320](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1320)

## [0.43.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.42.3...v0.43.0) (2025-06-27)


### Features

* **ldap-notifier:** Implement correct handling of pull policy configuration ([c8059f9](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/c8059f97728922f8a0ad96c257a3326cc7778ce9)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-notifier:** Update version of nubus-common to 0.21.0 ([7306cc4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/7306cc4f6aea947b3146180745cf955e6a2bb4be)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Adjust handling of "nats.auth" to common secrets structure ([e7f271a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/e7f271aa2b98ea5e853d95e4045c291ea85b528a)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Adjust Nats configuration to line up with common secret structure ([6846b24](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/6846b2457d8e607fb4989bac0b60a2c5d2f9687f)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Change image pull policy configuration to "image.pullPolicy" ([ad040a1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/ad040a1767b45b49440192480410ad585f9a0202)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Change secret name for the admin username ([891120b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/891120b37445110a3ee71330f332e847a581a604)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Ensure that the same password value is generated as before. ([40f7eeb](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/40f7eebcf0c90b1755ba5803528deaadceee151a)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Generated secret for ldap access follows common structure ([1b9b4ae](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/1b9b4aee32fd92c8f4824807d35cd6adb0166cbc)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Remove password environment variables in ldif-producer ([759f7ea](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/759f7ea05117ea9617add045c1a7a5783ab7c3a5)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Render the Nats secret only when ldif-producer is enabled ([2366f02](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/2366f02f35901e4784abab02376db3c86f362f95)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)


### Bug Fixes

* **ldap-notifier:** Correct handling of labels and annotations ([25be0a6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/25be0a656c4c4265431656b4fd11e58ef82bb1d6)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Avoid using the manage template when existingSecret is provided ([0f4e61b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/0f4e61b3f5a8aa4dcae99ef878078224101d8023)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Correct handling of labels and annotations ([3cdd09f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/3cdd09f9a09eee3e4da5a5000957749204a64204)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **ldap-server:** Respect the setting "global.secrets.keep" in the ldap secret ([1bfd7e7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/1bfd7e79b58853ab090b27ceec072e0f09c44cb4)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)

## [0.42.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.42.2...v0.42.3) (2025-06-26)


### Bug Fixes

* add sonarqube ([2924d28](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/2924d28076b7237b758a70f12322199250017d24)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)

## [0.42.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.42.1...v0.42.2) (2025-06-23)


### Bug Fixes

* trigger release ([ba6d74c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/ba6d74c85faccffd720127136a8d0a4ecf127c61)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/issues/0)

## [0.42.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/compare/v0.42.0...v0.42.1) (2025-06-18)


### Bug Fixes

* bump umc-base-image version ([13ce7bc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/ldap/commit/13ce7bca55d0fb6d84417ba9cef75e5555a223b5)), closes [univention/dev/internal/team-nubus#1263](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1263)

## [0.42.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.41.0...v0.42.0) (2025-06-09)


### Features

* updated ucs-base-image to 0.18.1-build-2025-05-29 ([d28c1c4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d28c1c44657b971bc408e978ff864eaf1cd90524)), closes [univention/dev/internal/team-nubus#1220](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1220)

## [0.41.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.40.0...v0.41.0) (2025-05-23)


### Features

* **ldap-server:** Add the univentionObjectIdentifier attribute to all relevant LDAP objects created from the base.ldif ([d721f5c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d721f5cd4b5d14e37b4b678947909d1060992ae9))


### Bug Fixes

* Copied base.ldif to prepare adding a patch to it ([2915fe4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2915fe45c85f16663220937b2806011924165e87))
* **ldap-server:** Fix bug of inline delimiters in UCR templates ([a7f9324](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a7f93240fb7b99a21898e006c8cd838112b7e0ed))

## [0.40.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.39.0...v0.40.0) (2025-05-15)


### Features

* add creation of cn=blocklists to init-internal-database.sh ([5bbef9b](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/5bbef9b7012baa9f1db1578c7fa275bd075a6e67))

## [0.39.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.38.1...v0.39.0) (2025-05-11)


### Features

* move and upgrade ucs-base-image to 0.17.3-build-2025-05-11 ([c721ace](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/c721ace02e65e6ceedf9e59e91687fc6858c8f80))

## [0.38.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.38.0...v0.38.1) (2025-05-10)


### Bug Fixes

* move addlicense pre-commit hook ([4cd37ae](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/4cd37ae06beced5851546916464f30db7c4bfbc1))
* move docker-services ([bec2add](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bec2adda924f5fd1b64bdf377fe4be136cf5ab1b))
* update common-ci to main ([e1c1c45](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e1c1c45a2ccba1285d3c11970cfbd3c9a08f6a5b))

## [0.38.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.37.0...v0.38.0) (2025-05-05)


### Features

* **ldap-server:** Adds switch to (de)activate index update on startup. ([a7c9be8](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a7c9be871be6a679b3f209d724e8d408f2ceb03e)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)

## [0.37.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.36.0...v0.37.0) (2025-04-29)


### Features

* Bump ucs-base-image version ([00f3870](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/00f387069661592f7783dbac8e1d212aefc747ae)), closes [univention/dev/internal/team-nubus#1155](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1155)


### Bug Fixes

* final version of wait-for-dependency ([45d2c49](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/45d2c49a7171922e69b0cca9b26760c6edb8d7b8)), closes [univention/dev/internal/team-nubus#1155](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1155)

## [0.36.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.35.0...v0.36.0) (2025-04-29)


### Features

* Remove docker.io dependencies ([ad8552f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ad8552f245c82cd3b86ce3f02640ed38cb0abaab)), closes [univention/dev/internal/team-nubus#1131](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1131)

## [0.35.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.34.3...v0.35.0) (2025-04-28)


### Features

* Added logging, changed  entrypoint, some refactoring ([0f58d87](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/0f58d870561776d79b08fe01c05d5988b64f57cf)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* Added more UnitTests ([200f5ec](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/200f5ecc7350b3722b0989e086734cc8823db37e)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* Added new env variable with default value PYTHON_LOG_LEVEL ([05dafaf](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/05dafafa6bed578f8b98773d5de8ce92482aff46)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* Added update statefile ([083b699](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/083b6997af905d2e573183af9eb5e9d72af9e183)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* LDAP index sync first draft ([3e28204](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3e28204d4984ba946a954221d94a4b831157ef69)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* LDAP index sync first working version ([66e12e6](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/66e12e6554d79394da2e23f67caaefd0107b2432)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* LDAP indexes added unittests ([f7ecdec](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f7ecdec401d00b4336b8dd28d5637a8774d8b72d)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)


### Bug Fixes

* **ldap-server:** Added test for LDAP index syncronisation. ([18b43a4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/18b43a4779275241fc785a3fa2705e300bd652fe)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **ldap-server:** Fixed docker unittest ([7a58d33](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/7a58d33d76baf39d33775d90e23ccd0f48a3c5be)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **ldap-server:** Fixed get_changed_attributs_call. ([7484124](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/74841249da3d50d48213fc32e919b8b025250242)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **ldap-server:** Multiple QA changes. ([51e50c1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/51e50c15e16aea5233dec6b7a20f5085e9f1d730)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **ldap-server:** Refacoring smoketest ([01b5961](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/01b5961362efeffccb0709ba3b6e5fff9e08d22a)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **ldap-server:** Refactoring and resilience in case of broken statefile syntax and missing env variables ([118bb92](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/118bb920d35fe6d44479b8792ad6b354b6a1b952))
* **ldap-server:** Refactoring logger f-strings to modulo operator ([9ac7bbc](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9ac7bbcf235504d413493fe6031a5b0c1b8bda5b)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* Pipeline fixed + renaming ([de72700](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/de72700715a6ae7866e33bd335677def2e7c8116)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **test:** Modified logger configuration. ([7c0ac17](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/7c0ac17a519aaad6020eccbf69e247905a2e7763)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* **tests:** Changed image to testrunner for ldap-sync-test. ([835629b](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/835629b32a9e2d860343ef8cb6f60816a018a5b7)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019) [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)
* UnitTests and refactoring ([45b4226](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/45b42268795eaa22c84cc02d950ad4afa9127db1)), closes [univention/dev/internal/team-nubus#1019](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1019)

## [0.34.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.34.2...v0.34.3) (2025-04-11)


### Bug Fixes

* typo in deployment-proxy-yaml ([5bc9461](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/5bc9461da6a9e737252379d20ff0f3edd2883b97)), closes [univention/dev/internal/team-nubus#1079](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1079)

## [0.34.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.34.1...v0.34.2) (2025-04-11)


### Bug Fixes

* directory robustness in initContainers of secondary LDAP ([bca99ea](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bca99eab84369736b9a667e9973dffe81204cb45))

## [0.34.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.34.0...v0.34.1) (2025-04-04)


### Bug Fixes

* LDAP – Resources not rendered correctly ([4e2b521](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/4e2b5211b0b21323f08076a4b9cd91bbe25ec4de)), closes [univention/dev/internal/team-nubus#1117](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1117)

## [0.34.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.33.3...v0.34.0) (2025-04-04)


### Features

* refactor: use existingSecrets for ldap-server and ldif-producer ([9238344](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/923834479bf8745f45247dcb0190a801aa8c0286)), closes [univention/dev/internal/team-nubus#1089](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1089)

## [0.33.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.33.2...v0.33.3) (2025-03-21)


### Bug Fixes

* namespace template in serviceacount ([fb891db](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fb891dbe2b0d5fe8603b68b3e9fe1ab7dce6f4c2)), closes [univention/dev/internal/team-nubus#1075](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1075)

## [0.33.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.33.1...v0.33.2) (2025-03-19)


### Bug Fixes

* **ldap-notifier:** added pod affinity so that ldap-notifier affines to ldap-server with index 0 ([50033aa](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/50033aa12c6dfcf03ad6a5aaeeeb60f0ef4a5a7c)), closes [univention/dev/internal/team-nubus#1077](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1077)

## [0.33.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.33.0...v0.33.1) (2025-03-11)


### Bug Fixes

* Also create Service ldap-server-primary-0 in scaled down deployments ([5b750e9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/5b750e97683eede659e53ba8d05e5c2e76399034))
* Make copy calls in init containers more robust ([2260510](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/226051073ec2ce61a65b8cc97e2921be11d901c6))

## [0.33.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.32.2...v0.33.0) (2025-02-26)


### Features

* Bump ucs-base-image to use released apt sources ([bb86716](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bb86716317b4ed78c3d5e1d805654dfbec650022))

## [0.32.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.32.1...v0.32.2) (2025-02-10)


### Bug Fixes

* set plugin mounts to read-only ([4dbecbf](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/4dbecbf222d968ba458f76bdb30804590359160f))

## [0.32.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.32.0...v0.32.1) (2025-02-10)


### Bug Fixes

* add .kyverno to helmignore ([1389a4c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1389a4cd4a30b6e7b5069ed4e393dafe91dad9a2))

## [0.32.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.31.1...v0.32.0) (2024-12-20)


### Features

* upgrade UCS base image to 2024-12-12 ([252852b](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/252852b7420991877829ec5a28f805e91f2755a8))

## [0.31.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.31.0...v0.31.1) (2024-12-19)


### Bug Fixes

* **leader-elector:** Overwrite the labelSelector on the primary service every 15 seconds to recover from initial state after the service is overwritten by helm ([58a0343](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/58a0343ed8fc3f85733056f66ab343fe7ed6642f))

## [0.31.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.30.0...v0.31.0) (2024-12-11)


### Features

* Avoid echoing the commands in shell scripts by default ([2ca48d1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2ca48d11e36fd919b1bc323bf13e043389c78c43))

## [0.30.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.29.1...v0.30.0) (2024-12-10)


### Features

* Explicit opt-in to enable the status ConfigMap ([ccc4a54](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ccc4a545cb067fcab329eb0dfb9f7b110c2a6462))

## [0.29.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.29.0...v0.29.1) (2024-12-10)


### Bug Fixes

* kyverno lint for ldap-server ([5648b79](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/5648b7916c8ca5968f4ee8ecc3a41bdf95471cb0))

## [0.29.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.28.0...v0.29.0) (2024-12-09)


### Features

* Add "managed-by" label to the status ConfigMap ([0b157f5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/0b157f5c995a6269eba77b13423ef95a0fa523ad))
* Add debug logging into the get_or_create function ([59ae0d4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/59ae0d4bfa655483c7143e007a93122cdd85ed42))
* Add dependencies via pipenv ([0a1be10](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/0a1be108253a9ef6d943bf01a1e36a3b5fabf280))
* Add environment variable "LDAP_SERVER_ROLE" ([3b1a2c8](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3b1a2c807f29ad5ed167550d9150669e95f8b949))
* Add logging output around database initialization in entrypoint script ([c293812](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/c293812fccdefc279d4757f801c553cd052cb63e))
* Allow to configure the configmap name via cli and environment variable ([6b3fdfa](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/6b3fdfa7afa743a4fb1b4228ef47fa49a6a9b114))
* Allow to configure the namespace via environment variable STATUS_NAMESPACE ([42e281a](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/42e281aa9ed032f63d1784da5c345bc2a141a3b9))
* Create the status ConfigMap if needed ([16c1fed](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/16c1fed794be6b70e94910c577bb215bfc448eab))
* Do not remove the Apt related artifacts ([adeea9a](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/adeea9acc3e637bc11aafd199ef2c43497e6cdd8))
* **leader-elector:** Check if an LDAP database is present before trying to become leader ([8e6c24e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/8e6c24ee078bcd706b61df54855c9e4fb719d67a))
* Only load initial content if "LDAP_SERVER_ROLE" is "primary" or unset ([3b6ab9c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3b6ab9c1d2c81d2eda0cfe168706a3a17b4306a8))
* Remove echoing of commands in additional entrypoint scripts of ldap-server ([5b70abe](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/5b70abe887196976edb2b53b6f11b5224c738d98))
* Stop dumping all environment variables on startup ([002608f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/002608f62c527d743411b6c2405d926e0d735783))
* Stop dumping the full configuration to standard output ([80b14be](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/80b14befa595519b3fc2a16c97cb183a119a43cd))
* Stop echoing the slapd.conf to stdout ([281ff68](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/281ff6803862f933570f36e1c1a8f21e20316d6f))
* Stop tracing all commands in "40-self-service-acl" ([d055274](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d05527491708df15db09289e5f8652fa4b1e92f2))
* Stop tracing all shell commands in the entrypoint of ldap-server ([e43bffa](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e43bffad1fa7dbc73e482a103df7cb460076363e))
* Update ucs base image to version 0.13.3-build-2024-12-05 ([6f287a9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/6f287a9b8862b8710d5ba9dfb5c567f50c030300))
* Validate the status data using a Pydantic model ([98bebe1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/98bebe16ed4342fde1af8602ea2baab6e6bf18ea))


### Bug Fixes

* Add docstring to subcommand "database-initialized" ([fe7d8c1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fe7d8c1abbec09fa8815371ca7eec1297edc2914))
* Adjust the Role permissions so that the status ConnfigMap can be created ([fb850c0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fb850c015282ef035989bbb842e6978d678c4cf9))
* Configure logging to print timestamps ([77c5496](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/77c5496a10c7101df0af53e242b458d497f6a83d))
* Correct capturing of exit code in entrypoint script ([c07d730](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/c07d730a3b96e4ad8b15e1c93aa9563372d30aaa))
* Correct handling of empty ConfigMap ([19e1b35](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/19e1b3526478aa36381f9e54db68156057217d1d))
* Correct usage of the logging api ([9d1777a](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9d1777a51f299592a4c8633cf6cc49a7eba21f0b))
* Disable configMap script in docker compose to fix the ldap smoke tests ([28cd2f0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/28cd2f0b7a7b980dbdea0f268b5a205c29ff10ca))
* Fail if the database status cannot be evaluated ([d056597](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d0565970538c5ed65ec607c254aedfef349787dc))
* fix linter warnings ([45e18d5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/45e18d5bcc94b33a2921823a5656bbb24b11c63a))
* fix unit tests ([78a7cab](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/78a7cab685ad147e5d598113d79f1996c0824d7e))
* **ldap-server:** Add intitialization script to Dockerfile ([2cecdbc](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2cecdbc70dd4ae827748e8c7c3052fe2b27e2757))
* **ldap-server:** Check LDAP database initialization flag in configmap ([bf0bc66](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bf0bc668554de26b914d2bfa6c6d9ead49d409ff))
* **ldap-server:** improve LDAP database initialization script with log level and more ([9e56539](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9e56539e511cdd51c973981701184c4e8dca6675))
* **ldap-server:** LDAP database initialization in mirror-mode ([be4e879](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/be4e8798d3facb1c6402936d618e41445aa99e8d))

## [0.28.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.27.0...v0.28.0) (2024-12-04)


### Features

* **ldap-server:** Add service for ldap-server-primary-0 to be used by listeners ([8256526](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/82565263a8ac56bd5c30a4f566f4289e0e9b4f68))


### Bug Fixes

* **ldap-server:** Do not match any Pod until a leader claims the lead ([93e8336](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/93e8336668a0b156d52bfa73d987198494d0d205))
* **ldap-server:** ldap-primaries cannot see each other without a headless service for mirror mode ([04e8ae6](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/04e8ae6bc4290ce0b8536ece3cea354d3113a52e))
* **ldap-server:** multiprovider instead of mirrormode as of openldap 2.5 ([035712e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/035712eddbb6d79f8524774c652ec96fb710debb))
* **ldap-server:** serverID must be sequential starting from non 0 ([1dea0c2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1dea0c2ecd5dc8d26b6fafea40cd4e13f3787bd5))
* **ldap-server:** Update bitnami common source ([765b2bd](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/765b2bdd00ba8dbfd5f9eb05032e532e39c14593))

## [0.27.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.26.5...v0.27.0) (2024-11-28)


### Features

* improve leader election and ldap server configuration ([f743a52](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/f743a527fe0f3fea32a08fe8c735d81e2fa32689))
* ldap leader election ([70e8e65](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/70e8e656cf56205849eec8f24f0f1d05f73d510d))
* leader-elector container ([e5b3b28](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e5b3b28833c86a0186a4708ea4fd6b7665d0d326))
* make ldap-server-primary service headed ([ed5c96e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ed5c96e4cfa6bbbc6d1283204a3c1eaadf8f15e3))


### Bug Fixes

* apply leader_elector.py suggestions ([9ded5e9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9ded5e966eee9dd1c94a8b555456a79c67b20e6b))
* handle SIGTERM ([9cc6bc2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9cc6bc282a4dbae71d9e0c5dc0a2d32b3ffa9aa0))
* kyverno lint values ([3957228](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/3957228500995110b484c51067e91037950bbecc))

## [0.26.5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.26.4...v0.26.5) (2024-11-25)


### Bug Fixes

* add a systemExtension to the linter_values.yaml file ([9e9bcdd](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9e9bcdd0acd9bd4ed0c162429ad74787ef0079d3))
* kyverno lint ([23f9406](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/23f94062acfda5e547e042b29717d7e1a8a2ae85))

## [0.26.4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.26.3...v0.26.4) (2024-11-20)


### Bug Fixes

* **ldap-server:** remove file ownership errors in the univention-compatibility initContainer ([237d1f3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/237d1f39acc59af5fb7462e811378a6b8435e751))

## [0.26.3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.26.2...v0.26.3) (2024-11-01)


### Bug Fixes

* add digest to wait-for-dependency image tag ([fe42efb](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fe42efb63232bf1aa33b3f93256b6c37a903967c))

## [0.26.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.26.1...v0.26.2) (2024-10-02)


### Bug Fixes

* **ldif-producer:** fix typo leading to missing DN in log ([9f0705a](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/9f0705a55cc53243bbfa801817ffa48d3e749eab))

## [0.26.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.26.0...v0.26.1) (2024-10-01)


### Bug Fixes

* **ci:** use kaniko for building the ldap-notifier image ([76bfab1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/76bfab1494918cd871101708f786ad9302b61dea))

## [0.26.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.25.2...v0.26.0) (2024-09-26)


### Features

* **ci:** enable malware scanning, disable sbom generation ([ab19c5f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ab19c5fcdd306c7befe26edf54a5ebc8728122d5))

## [0.25.2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.25.1...v0.25.2) (2024-09-23)


### Bug Fixes

* configuration name consistency ([6e31dd2](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/6e31dd2e7f54cc75f441f7d546dcddca2bbce8fb))

## [0.25.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.25.0...v0.25.1) (2024-09-23)


### Bug Fixes

* **ldap-server:** Don't leak secrets in bash scripts ([5cddbb3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/5cddbb3105e01c77e0de415465869774520fa6d2))

## [0.25.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.24.0...v0.25.0) (2024-09-16)


### Features

* update UCS base image to 2024-09-09 ([59d4f84](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/59d4f8494270d67a60d1c28201da4d802bc33fc7))
* upgrade wait-for-dependency image ([dcae7c7](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/dcae7c71bc6b4513dc0757e4d1325ad7399c2bf8))

## [0.24.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.23.0...v0.24.0) (2024-09-06)


### Features

* add support for extraInitContainers ([612579f](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/612579f6df96e5204110631c37b1c0c502560ab8))
* changes relating to BSI compliance ([a94a0f8](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a94a0f87f03fca30686ff6c45c79ccaf6376f2f1))


### Bug Fixes

* remove testrunner from list of containers to sign ([ef5939c](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/ef5939ce3a993f116536cd9123f9a005df7ec02a))

## [0.23.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.22.1...v0.23.0) (2024-08-28)


### Features

* unify UCR configuration ([dc68ddb](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/dc68ddb22c9daacdb3d3886f81f050b5707bdc87))

## [0.22.1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.22.0...v0.22.1) (2024-08-19)


### Bug Fixes

* initialize queue with the 'WorkQueuePolicy' RetentionPolicy ([fec8810](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fec881023122bbf2c8596ce7033b6158301e650a))
* update provisioning consumer client ([2288bf1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/2288bf1c53d99944a14ae4a9955d69384a83cdb7))

## [0.22.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.21.0...v0.22.0) (2024-07-25)


### Features

* **ldif-producer:** use async slapdsock, simplify project structure ([60b0178](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/60b01786c61573e3da536bffd0988f5edffd309d))
* **ldif-producer:** use asyncio streams instead of sockserver with threading ([1c7e5b1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/1c7e5b15b0492d79f22d2ae1ada879bbc581b7fa))
* send message and request IDs ([af813f0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/af813f0973d80eb8cd7d63a598a8fac5d7e597a1))


### Bug Fixes

* improve logging ([dc66be3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/dc66be3e348b346b1ef5d7d70516e10e2362f4d1))
* **ldif-producer:** don't accept socket requests if the nats connection is not (yet) active ([6ea8e3d](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/6ea8e3d064f7b1b282d8941c46ec7fb4d39e036e))
* **ldif-producer:** don't log expected behavior ([fdd0ddb](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/fdd0ddbdd25fc3a790811a906d8f7b13a9ae9fb3))
* **ldif-producer:** don't respond to empty requests ([e3cf94e](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e3cf94efb397cb3adef8de6ab2b31e04c7d2df15))
* **ldif-producer:** fix container entrypoint and remove default arguments ([52aeea5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/52aeea556fafe80bda4fddf2d03922b1f6a91b13))
* **ldif-producer:** fix typos ([8db24b8](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/8db24b828df7ba2f99a5f1b8527676d622d17511))
* **ldif-producer:** improvements with Arvid ([a6cbcc9](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/a6cbcc9e97ee1f64b8f4e4e4920311f2cd4701e1))
* **ldif-producer:** make request_throttling non-blocking to not block forever if the outgoing_queue is full ([96f21a3](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/96f21a3767d16aaaff22ddbce90fd2a3fc531f32))
* **ldif-producer:** propperly instantiate the two coroutines with a task group ([cc2c68b](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/cc2c68be3f5fe3a4a8fdc79b12bf01cc2c1e1e99))
* **ldif-producer:** shorten log lines ([49a33a5](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/49a33a500008022f33340fc2988b397e7517dc89))

## [0.21.0](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/compare/v0.20.1...v0.21.0) (2024-07-19)


### Features

* **ldap-server:** load, activate and configure the back-sock overlay in the ldap-server slapd.conf ([99fa529](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/99fa5292221b1b2053720ac08c3856a207d872f1))
* **ldif-producer:** add the ldif-producer sidecar container to the ldap-server helm chart ([d13e4b1](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/d13e4b123da5ef157d278225fe5531fafcb48a14))
* **ldif-producer:** new, more reliable backpressure mechanism without pre- and post-hook synchronization ([7187c60](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/7187c60ca3af212b0e92f4bd5caf5f341ba36835))


### Bug Fixes

* **ldif-producer:** improvements with Arvid ([dea6176](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/dea61767271a47c76962b4a9ad4a7386b94469d9))
* **ldif-producer:** log exception tracebacks ([e681532](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e6815325329f521c18c35bed4f5eb3ab46c71ac8))
* **ldif-producer:** make existing backpressure-mechanism non-blocking ([e3e9454](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/e3e9454b06b56c6d887a33f9ebadcf2d77df6a1c))
* **ldif-producer:** put the ldif-producer and slapd-sock overlay behind a feature-flag ([cfdbded](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/cfdbdeda0291393a717c6d1e8aead199e84247cc))
* **ldif-producer:** return Continue for requests with empty body and improve logging ([bc0a7f4](https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/commit/bc0a7f46169730708cda659e953be8efb5fff127))

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

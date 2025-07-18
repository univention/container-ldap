# ldap-server

A Helm Chart that deploys a standalone OpenLDAP server

- **Version**: 0.11.0
- **Type**: application
- **AppVersion**:
-

## TL;DR

```console
helm upgrade --install ldap-server oci://gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/container-ldap/helm/ldap-server
```

## Introduction

This chart does install the OpenLDAP server.

## Installing

To install the chart with the release name `ldap-server`:

```console
helm upgrade --install ldap-server oci://gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/container-ldap/helm/ldap-server
```

## Uninstalling

To uninstall the chart with the release name `ldap-server`:

```console
helm uninstall ldap-server
```

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://artifacts.software-univention.de/nubus/charts | nubus-common | 0.21.0 |

## Values

<table>
	<thead>
		<th>Key</th>
		<th>Type</th>
		<th>Default</th>
		<th>Description</th>
	</thead>
	<tbody>
		<tr>
			<td>additionalAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom annotations to add to all deployed objects.</td>
		</tr>
		<tr>
			<td>additionalLabels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom labels to add to all deployed objects.</td>
		</tr>
		<tr>
			<td>affinityPrimary</td>
			<td>object</td>
			<td><pre lang="json">
{
  "podAntiAffinity": {
    "preferredDuringSchedulingIgnoredDuringExecution": [
      {
        "podAffinityTerm": {
          "labelSelector": {
            "matchExpressions": [
              {
                "key": "ldap-server-type",
                "operator": "In",
                "values": [
                  "primary"
                ]
              }
            ]
          },
          "topologyKey": "kubernetes.io/hostname"
        },
        "weight": 100
      }
    ]
  }
}
</pre>
</td>
			<td>Affinity for pod assignment. Ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity Note: podAffinityPreset, podAntiAffinityPreset, and nodeAffinityPreset will be ignored when it's set.</td>
		</tr>
		<tr>
			<td>affinityProxy.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key</td>
			<td>string</td>
			<td><pre lang="json">
"ldap-server-type"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinityProxy.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator</td>
			<td>string</td>
			<td><pre lang="json">
"In"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinityProxy.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0]</td>
			<td>string</td>
			<td><pre lang="json">
"proxy"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinityProxy.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey</td>
			<td>string</td>
			<td><pre lang="json">
"kubernetes.io/hostname"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinityProxy.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight</td>
			<td>int</td>
			<td><pre lang="json">
100
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinitySecondary.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key</td>
			<td>string</td>
			<td><pre lang="json">
"ldap-server-type"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinitySecondary.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator</td>
			<td>string</td>
			<td><pre lang="json">
"In"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinitySecondary.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0]</td>
			<td>string</td>
			<td><pre lang="json">
"secondary"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinitySecondary.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey</td>
			<td>string</td>
			<td><pre lang="json">
"kubernetes.io/hostname"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinitySecondary.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight</td>
			<td>int</td>
			<td><pre lang="json">
100
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>containerSecurityContext.allowPrivilegeEscalation</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>Enable container privileged escalation.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.capabilities</td>
			<td>object</td>
			<td><pre lang="json">
{
  "drop": [
    "ALL"
  ]
}
</pre>
</td>
			<td>Security capabilities for container.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enable security context.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.privileged</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>containerSecurityContext.readOnlyRootFilesystem</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Mounts the container's root filesystem as read-only.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.runAsGroup</td>
			<td>int</td>
			<td><pre lang="json">
102
</pre>
</td>
			<td>Process group id.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.runAsNonRoot</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Run container as a user.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.runAsUser</td>
			<td>int</td>
			<td><pre lang="json">
101
</pre>
</td>
			<td>Process user id.</td>
		</tr>
		<tr>
			<td>containerSecurityContext.seccompProfile.type</td>
			<td>string</td>
			<td><pre lang="json">
"RuntimeDefault"
</pre>
</td>
			<td>Disallow custom Seccomp profile by setting it to RuntimeDefault.</td>
		</tr>
		<tr>
			<td>dhInitContainer.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>dhInitContainer.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
"docker.io"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>dhInitContainer.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"alpine/openssl"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>dhInitContainer.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"3.1.4@sha256:974b4593b02447256622dce7b930b98764441dab39c5ca729381aa35332d6778"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>extensions</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Extensions to load. This will override the configuration in `global.extensions`.</td>
		</tr>
		<tr>
			<td>extraEnvVars</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Array with extra environment variables to add to containers.  extraEnvVars:   - name: FOO     value: "bar"</td>
		</tr>
		<tr>
			<td>extraSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Optionally specify a secret to create (primarily intended to be used in development environments to provide custom certificates)</td>
		</tr>
		<tr>
			<td>extraVolumeMounts</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Optionally specify an extra list of additional volumeMounts.</td>
		</tr>
		<tr>
			<td>extraVolumes</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Optionally specify an extra list of additional volumes.</td>
		</tr>
		<tr>
			<td>fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Provide a name to substitute for the full names of resources.</td>
		</tr>
		<tr>
			<td>global.configMapUcr</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>ConfigMap name to read UCR values from.</td>
		</tr>
		<tr>
			<td>global.extensions</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Allows to configure extensions globally.</td>
		</tr>
		<tr>
			<td>global.imagePullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Define an ImagePullPolicy.  Ref.: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy  "IfNotPresent" => The image is pulled only if it is not already present locally. "Always" => Every time the kubelet launches a container, the kubelet queries the container image registry to             resolve the name to an image digest. If the kubelet has a container image with that exact digest cached             locally, the kubelet uses its cached image; otherwise, the kubelet pulls the image with the resolved             digest, and uses that image to launch the container. "Never" => The kubelet does not try fetching the image. If the image is somehow already present locally, the            kubelet attempts to start the container; otherwise, startup fails.</td>
		</tr>
		<tr>
			<td>global.imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry"</td>
		</tr>
		<tr>
			<td>global.imageRegistry</td>
			<td>string</td>
			<td><pre lang="json">
"artifacts.software-univention.de"
</pre>
</td>
			<td>Container registry address.</td>
		</tr>
		<tr>
			<td>global.ldap.baseDn</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.ldap.domainName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.nats.connection.port</td>
			<td>string</td>
			<td><pre lang="json">
"4222"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.nubusDeployment</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>Indicates wether this chart is part of a Nubus deployment.</td>
		</tr>
		<tr>
			<td>global.systemExtensions</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Allows to configure system extensions globally.</td>
		</tr>
		<tr>
			<td>highAvailabilityMode</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>HA Mode If enabled, will override the replicaCountPrimary, replicaCountSecondary and replicaCountProxy values with the minimum viable values for a HA setup (if specified values are otherwise insufficient).</td>
		</tr>
		<tr>
			<td>imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry"</td>
		</tr>
		<tr>
			<td>ldapServer.auth</td>
			<td>object</td>
			<td><pre lang="json">
{
  "existingSecret": {
    "keyMapping": {
      "password": null
    },
    "name": null
  },
  "password": null
}
</pre>
</td>
			<td>LDAP admin user secret configuration</td>
		</tr>
		<tr>
			<td>ldapServer.config.domainName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Internal domain name of the UCS machine domainName: "univention-organization.intranet"</td>
		</tr>
		<tr>
			<td>ldapServer.config.ldapBaseDn</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Base DN of the LDAP directory ldapBaseDn: "dc=univention-organization,dc=intranet"</td>
		</tr>
		<tr>
			<td>ldapServer.config.logLevel</td>
			<td>string</td>
			<td><pre lang="json">
"stats"
</pre>
</td>
			<td>Log level for slapd.    Pass a comma-separated list of values from the <a href="https://openldap.org/doc/admin24/runningslapd.html#Command-Line%20Options">OpenLDAP docs</a>.    Example: `"conns,stats"`.</td>
		</tr>
		<tr>
			<td>ldapServer.config.pythonLogLevel</td>
			<td>string</td>
			<td><pre lang="json">
"INFO"
</pre>
</td>
			<td>Log level for Python.    Pass a value from the <a href="https://docs.python.org/3/library/logging.html#logging-levels">Python logging docs</a>.</td>
		</tr>
		<tr>
			<td>ldapServer.config.samlMetadataUrl</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>URL of the IdP that contains the SAML metadata. samlMetadataUrl: "http://myportal.local:8097/realms/ucs/protocol/saml/descriptor"</td>
		</tr>
		<tr>
			<td>ldapServer.config.samlMetadataUrlInternal</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Internal URL of the IdP to download SAML metadata from,    in the case that `saml_metadata_url` is not visible to the container. samlMetadataUrlInternal: "http://keycloak.myportal.local/realms/ucs/protocol/saml/descriptor"</td>
		</tr>
		<tr>
			<td>ldapServer.config.samlServiceProviders</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>A comma separated list of SAML2 Service Provider URLs (must be defined) samlServiceProviders: "http://myportal.local:8000/univention/saml/metadata,http://myportal.local:8000/auth/realms/ucs"</td>
		</tr>
		<tr>
			<td>ldapServer.config.updateIndexOnStartup</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Switch to (de)activate the ldap index syncronization on startup. (true/false)</td>
		</tr>
		<tr>
			<td>ldapServer.generateDHparam</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>ldapServer.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Container registry address. This setting has higher precedence than global.registry.</td>
		</tr>
		<tr>
			<td>ldapServer.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/ldap-server"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Container registry address. This setting has higher precedence than global.registry.</td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/ldap-server-elector"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.leaseDurationSeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.leaseName</td>
			<td>string</td>
			<td><pre lang="json">
"ldap-primary-leader"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.renewDeadlineSeconds</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.leaderElector.retryPeriodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.legacy.shareSamlSize</td>
			<td>string</td>
			<td><pre lang="json">
"100Mi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.legacy.sharedRunSize</td>
			<td>string</td>
			<td><pre lang="json">
"1Gi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.tls.caCertificateFile</td>
			<td>string</td>
			<td><pre lang="json">
"/certificates/ca.crt"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.tls.certificateFile</td>
			<td>string</td>
			<td><pre lang="json">
"/certificates/tls.crt"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.tls.certificateKeyFile</td>
			<td>string</td>
			<td><pre lang="json">
"/certificates/tls.key"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.tls.dhparam</td>
			<td>object</td>
			<td><pre lang="json">
{
  "existingSecret": {
    "keyMapping": {
      "dhparam.pem": null
    },
    "name": null
  }
}
</pre>
</td>
			<td>Optional reference to the secret to use for reading Diffie-Hellman parameters</td>
		</tr>
		<tr>
			<td>ldapServer.tls.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldapServer.tls.existingSecret</td>
			<td>object</td>
			<td><pre lang="json">
{
  "keyMapping": {
    "ca.crt": null,
    "tls.crt": null,
    "tls.key": null
  },
  "name": null
}
</pre>
</td>
			<td>Optional reference to the secret to use for reading certificates</td>
		</tr>
		<tr>
			<td>ldifProducer.config.backpressureWaitTimeout</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.config.ldapThreads</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Amount of socketserver worker threads, should be roughly equivalent to the amount of ldap threads.</td>
		</tr>
		<tr>
			<td>ldifProducer.config.logLevel</td>
			<td>string</td>
			<td><pre lang="json">
"INFO"
</pre>
</td>
			<td>Log level for the ldif-producer. valid values are: ERROR WARNING, INFO, DEBUG</td>
		</tr>
		<tr>
			<td>ldifProducer.config.maxInFlightLdapMessages</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>ldifProducer.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Container registry address. This setting has higher precedence than global.registry.</td>
		</tr>
		<tr>
			<td>ldifProducer.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/ldif-producer"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.auth.existingSecret.keyMapping.password</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.auth.existingSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
"ldif-producer"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.connection.host</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.connection.port</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldifProducer.nats.natsMaxReconnectAttempts</td>
			<td>int</td>
			<td><pre lang="json">
2
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>lifecycleHooks</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Lifecycle to automate configuration before or after startup.</td>
		</tr>
		<tr>
			<td>livenessProbe.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td>Number of failed executions until container is terminated.</td>
		</tr>
		<tr>
			<td>livenessProbe.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td>Delay after container start until LivenessProbe is executed.</td>
		</tr>
		<tr>
			<td>livenessProbe.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>Time between probe executions.</td>
		</tr>
		<tr>
			<td>livenessProbe.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of successful executions after failed ones until container is marked healthy.</td>
		</tr>
		<tr>
			<td>livenessProbe.tcpSocket.port</td>
			<td>int</td>
			<td><pre lang="json">
389
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>livenessProbe.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Timeout for command return.</td>
		</tr>
		<tr>
			<td>nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>String to partially override release name.</td>
		</tr>
		<tr>
			<td>nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Node labels for pod assignment. Ref: https://kubernetes.io/docs/user-guide/node-selection/</td>
		</tr>
		<tr>
			<td>persistence.accessModes</td>
			<td>list</td>
			<td><pre lang="json">
[
  "ReadWriteOnce"
]
</pre>
</td>
			<td>The volume access modes, some of "ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany", "ReadWriteOncePod".  "ReadWriteOnce" => The volume can be mounted as read-write by a single node. ReadWriteOnce access mode still can                    allow multiple pods to access the volume when the pods are running on the same node. "ReadOnlyMany" => The volume can be mounted as read-only by many nodes. "ReadWriteMany" => The volume can be mounted as read-write by many nodes. "ReadWriteOncePod" => The volume can be mounted as read-write by a single Pod. Use ReadWriteOncePod access mode if                       you want to ensure that only one pod across whole cluster can read that PVC or write to it. </td>
		</tr>
		<tr>
			<td>persistence.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Annotations for the PVC.</td>
		</tr>
		<tr>
			<td>persistence.dataSource</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Custom PVC data source.</td>
		</tr>
		<tr>
			<td>persistence.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enable data persistence (true) or use temporary storage (false).</td>
		</tr>
		<tr>
			<td>persistence.existingClaim</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Use an already existing claim.</td>
		</tr>
		<tr>
			<td>persistence.labels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Labels for the PVC.</td>
		</tr>
		<tr>
			<td>persistence.selector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Selector to match an existing Persistent Volume (this value is evaluated as a template).  selector:   matchLabels:     app: my-app </td>
		</tr>
		<tr>
			<td>persistence.size</td>
			<td>string</td>
			<td><pre lang="json">
"10Gi"
</pre>
</td>
			<td>The volume size with unit.</td>
		</tr>
		<tr>
			<td>persistence.storageClass</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The (storage) class of PV.</td>
		</tr>
		<tr>
			<td>podAnnotationsPrimary</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Pod Annotations. Ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/</td>
		</tr>
		<tr>
			<td>podAnnotationsProxy</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podAnnotationsSecondary</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podLabels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Pod Labels. Ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/</td>
		</tr>
		<tr>
			<td>podSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enable security context.</td>
		</tr>
		<tr>
			<td>podSecurityContext.fsGroup</td>
			<td>int</td>
			<td><pre lang="json">
102
</pre>
</td>
			<td>If specified, all processes of the container are also part of the supplementary group.</td>
		</tr>
		<tr>
			<td>podSecurityContext.fsGroupChangePolicy</td>
			<td>string</td>
			<td><pre lang="json">
"Always"
</pre>
</td>
			<td>Change ownership and permission of the volume before being exposed inside a Pod.</td>
		</tr>
		<tr>
			<td>podSecurityContext.sysctls</td>
			<td>list</td>
			<td><pre lang="json">
[
  {
    "name": "net.ipv4.ip_unprivileged_port_start",
    "value": "1"
  }
]
</pre>
</td>
			<td>Allow binding to ports below 1024 without root access.</td>
		</tr>
		<tr>
			<td>rbac.create</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Allows to disable the creation of "Role" and "RoleBinding".</td>
		</tr>
		<tr>
			<td>readinessProbe.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td>Number of failed executions until container is considered not ready.</td>
		</tr>
		<tr>
			<td>readinessProbe.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td>Delay after container start until ReadinessProbe is executed.</td>
		</tr>
		<tr>
			<td>readinessProbe.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>Time between probe executions.</td>
		</tr>
		<tr>
			<td>readinessProbe.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of successful executions after failed ones until container is marked healthy.</td>
		</tr>
		<tr>
			<td>readinessProbe.tcpSocket.port</td>
			<td>int</td>
			<td><pre lang="json">
389
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbe.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Timeout for command return.</td>
		</tr>
		<tr>
			<td>readinessProbePrimary.exec.command[0]</td>
			<td>string</td>
			<td><pre lang="json">
"/bin/sh"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbePrimary.exec.command[1]</td>
			<td>string</td>
			<td><pre lang="json">
"-c"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbePrimary.exec.command[2]</td>
			<td>string</td>
			<td><pre lang="json">
"ldapsearch -H ldapi:/// -Y EXTERNAL -b \"cn=config\" -LLL \"(\u0026(objectClass=mdb))\" dn"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>readinessProbePrimary.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of failed executions until container is considered not ready.</td>
		</tr>
		<tr>
			<td>readinessProbePrimary.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td>Delay after container start until ReadinessProbe is executed.</td>
		</tr>
		<tr>
			<td>readinessProbePrimary.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>Time between probe executions.</td>
		</tr>
		<tr>
			<td>readinessProbePrimary.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of successful executions after failed ones until container is marked healthy.</td>
		</tr>
		<tr>
			<td>readinessProbePrimary.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Timeout for command return.</td>
		</tr>
		<tr>
			<td>replicaCountPrimary</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Set the amount of replicas of the primary statefulset.</td>
		</tr>
		<tr>
			<td>replicaCountProxy</td>
			<td>int</td>
			<td><pre lang="json">
0
</pre>
</td>
			<td>Set the amount of replicas of the proxy deployment.</td>
		</tr>
		<tr>
			<td>replicaCountSecondary</td>
			<td>int</td>
			<td><pre lang="json">
0
</pre>
</td>
			<td>Set the amount of replicas of the secondary statefulset.</td>
		</tr>
		<tr>
			<td>resources</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>resourcesPrimary</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>resourcesProxy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>resourcesSecondary</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom annotations.</td>
		</tr>
		<tr>
			<td>service.ports.ldap.containerPort</td>
			<td>int</td>
			<td><pre lang="json">
389
</pre>
</td>
			<td>Internal port.</td>
		</tr>
		<tr>
			<td>service.ports.ldap.port</td>
			<td>int</td>
			<td><pre lang="json">
389
</pre>
</td>
			<td>Accessible port.</td>
		</tr>
		<tr>
			<td>service.ports.ldap.protocol</td>
			<td>string</td>
			<td><pre lang="json">
"TCP"
</pre>
</td>
			<td>service protocol.</td>
		</tr>
		<tr>
			<td>service.ports.ldaps.containerPort</td>
			<td>int</td>
			<td><pre lang="json">
636
</pre>
</td>
			<td>Internal port.</td>
		</tr>
		<tr>
			<td>service.ports.ldaps.port</td>
			<td>int</td>
			<td><pre lang="json">
636
</pre>
</td>
			<td>Accessible port.</td>
		</tr>
		<tr>
			<td>service.ports.ldaps.protocol</td>
			<td>string</td>
			<td><pre lang="json">
"TCP"
</pre>
</td>
			<td>service protocol.</td>
		</tr>
		<tr>
			<td>service.type</td>
			<td>string</td>
			<td><pre lang="json">
"ClusterIP"
</pre>
</td>
			<td>Choose the kind of Service, one of "ClusterIP", "NodePort" or "LoadBalancer".</td>
		</tr>
		<tr>
			<td>serviceAccount.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.automountServiceAccountToken</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.create</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.labels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom labels for the ServiceAccount.</td>
		</tr>
		<tr>
			<td>serviceAccount.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>startupProbe.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
10
</pre>
</td>
			<td>Number of failed executions until container is terminated.</td>
		</tr>
		<tr>
			<td>startupProbe.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td>Delay after container start until StartupProbe is executed.</td>
		</tr>
		<tr>
			<td>startupProbe.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>Time between probe executions.</td>
		</tr>
		<tr>
			<td>startupProbe.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td>Number of successful executions after failed ones until container is marked healthy.</td>
		</tr>
		<tr>
			<td>startupProbe.tcpSocket.port</td>
			<td>int</td>
			<td><pre lang="json">
389
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>startupProbe.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
5
</pre>
</td>
			<td>Timeout for command return.</td>
		</tr>
		<tr>
			<td>systemExtensions</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Allows to configure the system extensions to load. This is intended for internal usage, prefer to use `extensions` for user configured extensions. This value will override the configuration in `global.systemExtensions`.</td>
		</tr>
		<tr>
			<td>terminationGracePeriodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td>In seconds, time the given to the pod needs to terminate gracefully. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods</td>
		</tr>
		<tr>
			<td>tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Tolerations for pod assignment. Ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/</td>
		</tr>
		<tr>
			<td>topologySpreadConstraints</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Topology spread constraints rely on node labels to identify the topology domain(s) that each Node is in. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/  topologySpreadConstraints:   - maxSkew: 1     topologyKey: failure-domain.beta.kubernetes.io/zone     whenUnsatisfiable: DoNotSchedule</td>
		</tr>
		<tr>
			<td>updateStrategy.type</td>
			<td>string</td>
			<td><pre lang="json">
"RollingUpdate"
</pre>
</td>
			<td>Set to Recreate if you use persistent volume that cannot be mounted by more than one pods to make sure the pods are destroyed first.</td>
		</tr>
		<tr>
			<td>waitForDependency.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus/images/wait-for-dependency"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"0.35.0@sha256:61dfaea28a2b150459138dfd6a554ce53850cee05ef2a72ab47bbe23f2a92d0d"
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>


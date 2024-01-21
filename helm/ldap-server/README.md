# ldap-server

A Helm chart for the ldap-server

- **Version**: 0.1.0
- **Type**: application
- **AppVersion**: 2.4.47+dfsg-3+deb10u7A~5.0.1.202205211909
- **Homepage:** <https://www.univention.de/>

## TL;DR

```console
helm upgrade --install ldap-server oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/container-ldap/helm/ldap-server
```

## Introduction

This chart does install the OpenLDAP server.

## Installing

To install the chart with the release name `ldap-server`:

```console
helm upgrade --install ldap-server oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/container-ldap/helm/ldap-server
```

## Uninstalling

To uninstall the chart with the release name `ldap-server`:

```console
helm uninstall ldap-server
```

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/common-helm/helm | common | ^0.2.0 |

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
			<td>affinity</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>autoscaling.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>environment</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.configMapUcr</td>
			<td>string</td>
			<td><pre lang="json">
"stack-data-swp-ucr"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.configMapUcrDefaults</td>
			<td>string</td>
			<td><pre lang="json">
"stack-data-ums-ucr"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.configMapUcrForced</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"Always"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.pullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.registry</td>
			<td>string</td>
			<td><pre lang="json">
"gitregistry.knut.univention.de"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"univention/customers/dataport/upx/container-ldap/ldap-server"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.waitForDependency</td>
			<td>object</td>
			<td><pre lang="json">
{
  "imagePullPolicy": "Always",
  "registry": "gitregistry.knut.univention.de",
  "repository": "univention/components/univention-portal/wait-for-dependency",
  "sha256": "",
  "tag": "latest"
}
</pre>
</td>
			<td>Image to use for the dependency waiter</td>
		</tr>
		<tr>
			<td>image.waitForDependency.sha256</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>ldapServer</td>
			<td>object</td>
			<td><pre lang="json">
{
  "caCert": null,
  "caCertFile": "/var/secrets/ca_cert",
  "certPem": null,
  "certPemFile": "/var/secrets/cert_pem",
  "dhParam": null,
  "dhParamFile": "/var/secrets/dh_param",
  "environment": "production",
  "ldapSecret": null,
  "privateKey": null,
  "privateKeyFile": "/var/secrets/private_key",
  "waitForSamlMetadata": false
}
</pre>
</td>
			<td>Application configuration of the OpenLDAP server</td>
		</tr>
		<tr>
			<td>ldapServer.caCertFile</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/ca_cert"
</pre>
</td>
			<td>Path to the CA certificate.</td>
		</tr>
		<tr>
			<td>ldapServer.certPemFile</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/cert_pem"
</pre>
</td>
			<td>Path to the server certificate's public key in PEM format.</td>
		</tr>
		<tr>
			<td>ldapServer.dhParamFile</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/dh_param"
</pre>
</td>
			<td>Path to the DH parameters</td>
		</tr>
		<tr>
			<td>ldapServer.environment</td>
			<td>string</td>
			<td><pre lang="json">
"production"
</pre>
</td>
			<td>TODO: Clarify usage of this parameter</td>
		</tr>
		<tr>
			<td>ldapServer.ldapSecret</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Initial password to set for "cn=admin"</td>
		</tr>
		<tr>
			<td>ldapServer.privateKeyFile</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/private_key"
</pre>
</td>
			<td>Path to the server certificate's private key.</td>
		</tr>
		<tr>
			<td>ldapServer.waitForSamlMetadata</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>Whether to run an init container that waits for the IdP to be ready.</td>
		</tr>
		<tr>
			<td>nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>persistence.sharedData.size</td>
			<td>string</td>
			<td><pre lang="json">
"1Gi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>persistence.sharedData.storageClass</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>persistence.sharedRun.size</td>
			<td>string</td>
			<td><pre lang="json">
"1Gi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>persistence.sharedRun.storageClass</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>podSecurityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>replicaCount</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>resources</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>securityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.ports.ldap.port</td>
			<td>int</td>
			<td><pre lang="json">
389
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.ports.ldap.protocol</td>
			<td>string</td>
			<td><pre lang="json">
"TCP"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.sessionAffinity.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.sessionAffinity.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
10800
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.type</td>
			<td>string</td>
			<td><pre lang="json">
"ClusterIP"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>


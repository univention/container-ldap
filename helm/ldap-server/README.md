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
"registry.souvap-univention.de"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"souvap/tooling/images/univention-ldap/ldap-server"
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
  "domainname": "univention-organization.intranet",
  "environment": "production",
  "ldapBaseDn": "dc=univention-organization,dc=intranet",
  "ldapSecret": null,
  "ldapTlsCiphersuite": null,
  "logLevel": "stats",
  "privateKey": null,
  "privateKeyFile": "/var/secrets/private_key",
  "samlMetadataUrl": null,
  "samlMetadataUrlInternal": null,
  "samlServiceProviders": null,
  "tlsMode": "secure"
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
			<td>ldapServer.domainname</td>
			<td>string</td>
			<td><pre lang="json">
"univention-organization.intranet"
</pre>
</td>
			<td>Internal domain name of the UCS machine</td>
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
			<td>ldapServer.ldapBaseDn</td>
			<td>string</td>
			<td><pre lang="json">
"dc=univention-organization,dc=intranet"
</pre>
</td>
			<td>Base DN of the LDAP directory</td>
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
			<td>ldapServer.ldapTlsCiphersuite</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Set a custom OpenSSL ciphersuite (use `openssl ciphers -v $CIPHERSUITE` to test possible choices).    Default: `"HIGH:MEDIUM:!aNULL:!MD5:!RC4"`.</td>
		</tr>
		<tr>
			<td>ldapServer.logLevel</td>
			<td>string</td>
			<td><pre lang="json">
"stats"
</pre>
</td>
			<td>Log level for slapd.    Pass a comma-separated list of values from the <a href="https://openldap.org/doc/admin24/runningslapd.html#Command-Line%20Options">OpenLDAP docs</a>.    Example: `"conn,stats"`.</td>
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
			<td>ldapServer.samlMetadataUrl</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>URL of the IdP that contains the SAML metadata.</td>
		</tr>
		<tr>
			<td>ldapServer.samlMetadataUrlInternal</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Internal URL of the IdP to download SAML metadata from,    in the case that `saml_metadata_url` is not visible to the container.</td>
		</tr>
		<tr>
			<td>ldapServer.samlServiceProviders</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>A comma separated list of SAML2 Service Provider URLs</td>
		</tr>
		<tr>
			<td>ldapServer.tlsMode</td>
			<td>string</td>
			<td><pre lang="json">
"secure"
</pre>
</td>
			<td>TLS enabled/disabled.    Options: `"secure"`, `"off"`.</td>
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


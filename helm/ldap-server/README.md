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
| oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/common-helm/helm | common | ^0.1.0 |

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
			<td>image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ldap_server</td>
			<td>object</td>
			<td><pre lang="json">
{
  "ca_cert": null,
  "ca_cert_file": "/var/secrets/ca_cert",
  "cert_pem": null,
  "cert_pem_file": "/var/secrets/cert_pem",
  "domain_name": "univention-organization.intranet",
  "environment": "production",
  "ldap_admin_pw_hash": null,
  "ldap_base_dn": "dc=univention-organization,dc=intranet",
  "ldap_tls_ciphersuite": null,
  "private_key": null,
  "private_key_file": "/var/secrets/private_key",
  "saml_service_providers": null
}
</pre>
</td>
			<td>Application configuration of the OpenLDAP server</td>
		</tr>
		<tr>
			<td>ldap_server.ca_cert_file</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/ca_cert"
</pre>
</td>
			<td>Path to the CA certificate of the UCS machine.</td>
		</tr>
		<tr>
			<td>ldap_server.cert_pem_file</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/cert_pem"
</pre>
</td>
			<td>Path to the certificate of the LDAP server</td>
		</tr>
		<tr>
			<td>ldap_server.domain_name</td>
			<td>string</td>
			<td><pre lang="json">
"univention-organization.intranet"
</pre>
</td>
			<td>Internal domain name of the UCS machine</td>
		</tr>
		<tr>
			<td>ldap_server.environment</td>
			<td>string</td>
			<td><pre lang="json">
"production"
</pre>
</td>
			<td>TODO: Clarify usage of this parameter</td>
		</tr>
		<tr>
			<td>ldap_server.ldap_admin_pw_hash</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Hashed password to use for "cn=admin", must be "{CRYPT}". Example is generated via `slappasswd -h "{CRYPT}" -s univention`.</td>
		</tr>
		<tr>
			<td>ldap_server.ldap_base_dn</td>
			<td>string</td>
			<td><pre lang="json">
"dc=univention-organization,dc=intranet"
</pre>
</td>
			<td>Base DN of the LDAP directory</td>
		</tr>
		<tr>
			<td>ldap_server.ldap_tls_ciphersuite</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Set a custom ciphersuite. May be needed if gnutls instead of openssl is in use. Example `"NORMAL"`.</td>
		</tr>
		<tr>
			<td>ldap_server.private_key_file</td>
			<td>string</td>
			<td><pre lang="json">
"/var/secrets/private_key"
</pre>
</td>
			<td>Path to the private key file of the LDAP server</td>
		</tr>
		<tr>
			<td>ldap_server.saml_service_providers</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>A comma separated list of SAML2 Service Provider URLs</td>
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


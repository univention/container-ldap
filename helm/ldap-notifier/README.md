# ldap-notifier

A Helm chart for the ldap-notifier

- **Version**: 0.1.0
- **Type**: application
- **AppVersion**: 14.0.4
- **Homepage:** <https://www.univention.de/>

## TL;DR

```console
helm upgrade --install ldap-notifier oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/container-ldap/helm/ldap-notifier
```

## Introduction

This chart does install the Univention Directory Notifier.

## Installing

To install the chart with the release name `ldap-notifier`:

```console
helm upgrade --install ldap-notifier oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/container-ldap/helm/ldap-notifier
```

## Uninstalling

To uninstall the chart with the release name `ldap-notifier`:

```console
helm uninstall ldap-notifier
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
			<td>affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[0].key</td>
			<td>string</td>
			<td><pre lang="json">
"app.kubernetes.io/name"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[0].operator</td>
			<td>string</td>
			<td><pre lang="json">
"In"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[0].values[0]</td>
			<td>string</td>
			<td><pre lang="json">
"ldap-server"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey</td>
			<td>string</td>
			<td><pre lang="json">
"kubernetes.io/hostname"
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
"IfNotPresent"
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
"univention/customers/dataport/upx/container-ldap/ldap-notifier"
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
			<td>ldapNotifier</td>
			<td>object</td>
			<td><pre lang="json">
{
  "environment": "production"
}
</pre>
</td>
			<td>Application configuration for the Univention Directory Notifier</td>
		</tr>
		<tr>
			<td>ldapNotifier.environment</td>
			<td>string</td>
			<td><pre lang="json">
"production"
</pre>
</td>
			<td>TODO: Clarify usage of this parameter</td>
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
			<td>service.ports.notifier.port</td>
			<td>int</td>
			<td><pre lang="json">
6669
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service.ports.notifier.protocol</td>
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
		<tr>
			<td>volumes.claims</td>
			<td>object</td>
			<td><pre lang="json">
{
  "shared-data": "shared-data-ldap-server-0",
  "shared-run": "shared-run-ldap-server-0"
}
</pre>
</td>
			<td>Mapping of volumes to the volume claim names to use. Those have to match the volumes of the "ldap-server".</td>
		</tr>
	</tbody>
</table>


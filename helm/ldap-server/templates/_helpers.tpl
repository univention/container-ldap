{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions relate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
They are defined so other sub-charts can read information that otherwise would be solely known to this Helm chart.
If compatible Helm charts set .Values.global.nubusDeployment to true, the templates defined here will be imported.
*/}}
{{- define "nubusTemplates.ldapServer.ldap.connection.protocol" -}}
ldap
{{- end -}}

{{- define "nubusTemplates.ldapServer.ldap.connection.host" -}}
{{- printf "%s-ldap-server" .Release.Name -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.ldap.connection.port" -}}
389
{{- end -}}

{{- define "nubusTemplates.ldapServer.ldap.connection.uri" -}}
{{- printf "%s://%s-ldap-server" (include "nubusTemplates.ldapServer.ldap.connection.protocol" .) .Release.Name -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.ldap.baseDn" -}}
{{ if .Values.global.nubusDeployment }}
{{- required ".Values.global.ldap.baseDn must be set." .Values.global.ldap.baseDn -}}
{{- else -}}
{{- required ".Values.ldapServer.config.ldapBaseDn must be set." .Values.ldapServer.config.ldapBaseDn -}}
{{- end -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.ldap.domainName" -}}
{{- coalesce .Values.global.ldap.domainName | required "Either .Values.ldapServer.config.domainName or .Values.global.ldap.domainName must be set." -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.ldap.adminDn" -}}
{{- printf "cn=admin,%s" (include "nubusTemplates.ldapServer.ldap.baseDn" . ) -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.samlMetadataUrl" -}}
{{- include "ldap-server.samlMetadataUrl" . -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.samlMetadataUrlInternal" -}}
{{- include "ldap-server.samlMetadataUrlInternal" . -}}
{{- end -}}

{{- define "nubusTemplates.ldapServer.samlServiceProviders" -}}
{{- include "ldap-server.samlServiceProviders" . -}}
{{- end -}}

{{- /*
These template definitions are only used in this chart.
*/}}
{{- define "ldap-server.samlMetadataUrl" -}}
    {{- $protocol := "http" -}}
    {{- $keycloakService := printf "%s-keycloak" .Release.Name -}}
    {{- $keycloakServicePort := "8080" -}}
    {{- $nubusKeycloakDefaultRealm := "nubus" -}}
    {{- if and .Values.ldapServer .Values.ldapServer.config .Values.ldapServer.config.samlMetadataUrl -}}
        {{- .Values.ldapServer.config.samlMetadataUrl -}}
    {{- else if and .Values.global.keycloak .Values.global.keycloak.realm -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort .Values.global.keycloak.realm -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort $nubusKeycloakDefaultRealm -}}
    {{- else -}}
        {{- required ".Values.ldapServer.config.samlMetadataUrl must be defined." .Values.ldapServer.config.samlMetadataUrl -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.samlMetadataUrlInternal" -}}
    {{- $protocol := "http" -}}
    {{- $keycloakService := printf "%s-keycloak" .Release.Name -}}
    {{- $keycloakServicePort := "8080" -}}
    {{- $nubusKeycloakDefaultRealm := "nubus" -}}
    {{- if and .Values.ldapServer .Values.ldapServer.config .Values.ldapServer.config.samlMetadataUrlInternal -}}
        {{- .Values.ldapServer.config.samlMetadataUrlInternal -}}
    {{- else if and .Values.global.keycloak .Values.global.keycloak.realm -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort .Values.global.keycloak.realm -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort $nubusKeycloakDefaultRealm -}}
    {{- else -}}
        {{- required ".Values.ldapServer.config.samlMetadataUrlInternal must be defined." .Values.ldapServer.config.samlMetadataUrlInternal -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.samlServiceProviders" -}}
    {{- $protocol := "https" -}}
    {{- $nubusKeycloakDefaultSubdomain := "portal" -}}
    {{- if and .Values.ldapServer .Values.ldapServer.config .Values.ldapServer.config.samlServiceProviders -}}
        {{- .Values.ldapServer.config.samlServiceProviders -}}
    {{- else if and .Values.global.domain .Values.global.keycloak .Values.global.keycloak.subdomain -}}
        {{- printf "%s://%s.%s/univention/saml/metadata" $protocol .Values.global.keycloak.subdomain .Values.global.domain -}}
    {{- else if and .Values.global.nubusDeployment .Values.global.domain -}}
        {{- printf "%s://%s.%s/univention/saml/metadata" $protocol $nubusKeycloakDefaultSubdomain .Values.global.domain -}}
    {{- else -}}
        {{- required ".Values.ldapServer.config.samlServiceProviders must be defined." .Values.ldapServer.config.samlServiceProviders -}}
    {{- end -}}
{{- end -}}

{{- define "ldif-producer.nats.auth.credentialSecretName" -}}
{{- coalesce .Values.ldifProducer.nats.auth.credentialSecretName (printf "%s-ldif-producer-nats-credentials" .Release.Name) -}}
{{- end -}}

{{- define "ldap-server.credentialSecret" -}}
    {{- $name := default (printf "%s-credentials" (include "common.names.fullname" .)) .Values.ldapServer.credentialSecret.name -}}
    {{- $key := default "adminPassword" .Values.ldapServer.credentialSecret.key -}}

    {{- if and .Values.ldapServer.credentialSecret .Values.ldapServer.credentialSecret.name -}}
        name: {{ .Values.ldapServer.credentialSecret.name | quote }}
key: {{ .Values.ldapServer.credentialSecret.key | quote }}
    {{- else if .Values.global.nubusDeployment -}}
        name: {{ $name | quote }}
key: {{ $key | quote }}
    {{- else -}}
        name: {{ required ".Values.ldapServer.credentialSecret.name must be defined." .Values.ldapServer.credentialSecret.name | quote }}
key: {{ required ".Values.ldapServer.credentialSecret.key must be defined." .Values.ldapServer.credentialSecret.key | quote }}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.configMapUcr" -}}
    {{- $nubusConfigMapUcr := printf "%s-stack-data-ums-ucr" .Release.Name -}}
    {{- tpl (coalesce .Values.configMapUcr .Values.global.configMapUcr $nubusConfigMapUcr) . -}}
{{- end -}}

{{- define "ldap-server.ldap.connection.servicePrimary" -}}
{{ printf "%s-primary" (include "common.names.fullname" .) }}
{{- end -}}

{{- define "ldap-server.ldap.connection.uriPrimary" -}}
{{- printf "%s://%s" (include "nubusTemplates.ldapServer.ldap.connection.protocol" .) (include "ldap-server.ldap.connection.servicePrimary" .) -}}
{{- end -}}

{{- define "ldap-server.ldap.connection.serviceSecondary" -}}
{{ printf "%s-secondary" (include "common.names.fullname" .) }}
{{- end -}}

{{- define "ldap-server.ldap.connection.uriSecondary" -}}
{{- printf "%s://%s" (include "nubusTemplates.ldapServer.ldap.connection.protocol" .) (include "ldap-server.ldap.connection.serviceSecondary" .) -}}
{{- end -}}

{{- /*
Validates and returns the primary replica count.
Fails if replica count exceeds 2.
*/ -}}
{{- define "ldap-server.replicaCountPrimary" -}}
{{- $maxReplicas := 2 -}}
{{- if .Values.replicaCountPrimary -}}
  {{- $count := int .Values.replicaCountPrimary -}}
  {{- if gt $count $maxReplicas -}}
    {{- fail (printf "replica count %d exceeds maximum allowed value of %d" $count $maxReplicas) -}}
  {{- else if gt $count 1 -}}
    {{- $count -}}
  {{- else -}}
    {{- $count -}}
  {{- end -}}
{{- else if .Values.highAvailabilityMode -}}
  2
{{- else -}}
  1
{{- end -}}
{{- end -}}

{{- define "ldap-server.replicaCountSecondary" -}}
{{- if and .Values.replicaCountSecondary (gt (int .Values.replicaCountSecondary) 1) -}}
{{- int .Values.replicaCountSecondary -}}
{{- else if .Values.highAvailabilityMode -}}
3
{{- else -}}
{{- int .Values.replicaCountSecondary -}}
{{- end -}}
{{- end -}}

{{- define "ldap-server.replicaCountProxy" -}}
{{- if and .Values.replicaCountProxy (gt (int .Values.replicaCountProxy) 1) -}}
{{- int .Values.replicaCountProxy -}}
{{- else if .Values.highAvailabilityMode -}}
3
{{- else -}}
{{- int .Values.replicaCountProxy -}}
{{- end -}}
{{- end -}}


{{- define "ldap-server.service.selector.serverType" -}}
{{- if gt (int (include "ldap-server.replicaCountProxy" .)) 0 -}}
proxy
{{- else if gt (int (include "ldap-server.replicaCountSecondary" .)) 0 -}}
secondary
{{- else -}}
primary
{{- end -}}
{{- end -}}

{{- define "ldap-server.validateTerminationGracePeriod" -}}
{{- $leaseDuration := int .Values.ldapServer.leaderElector.leaseDurationSeconds -}}
{{- $terminationGracePeriod := 30 -}}
{{- if .Values.terminationGracePeriodSeconds -}}
  {{- $terminationGracePeriod = int .Values.terminationGracePeriodSeconds -}}
{{- end -}}
{{- if lt $terminationGracePeriod $leaseDuration -}}
  {{- fail (printf "terminationGracePeriodSeconds (%d) must be greater than or equal to ldapServer.leaderElector.leaseDurationSeconds (%d)" $terminationGracePeriod $leaseDuration) -}}
{{- end -}}
{{- end -}}

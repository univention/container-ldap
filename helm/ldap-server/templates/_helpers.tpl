{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions relate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
They are defined so other sub-charts can read information that otherwise would be solely known to this Helm chart.
If compatible Helm charts set .Values.global.nubusDeployment to true, the templates defined here will be imported.
*/}}
{{- define "nubusTemplates.ldap.protocol" -}}
ldap
{{- end -}}
{{- define "nubusTemplates.ldap.serviceName" -}}
{{- printf "%s-ldap-server" .Release.Name -}}
{{- end -}}

{{- /*
These template definitions are only used in this chart.
*/}}
{{- define "ldap-server.samlMetadataUrl" -}}
    {{- $protocol := "https" -}}
    {{- $keycloakService := printf "%s-keycloak" .Release.Name -}}
    {{- $keycloakServicePort := "8080" -}}
    {{- $nubusKeycloakDefaultRealm := "nubus" -}}
    {{- if .Values.ldapServer.config.samlMetadataUrl -}}
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
    {{- $protocol := "https" -}}
    {{- $keycloakService := printf "%s-keycloak" .Release.Name -}}
    {{- $keycloakServicePort := "8080" -}}
    {{- $nubusKeycloakDefaultRealm := "nubus" -}}
    {{- if .Values.ldapServer.config.samlMetadataUrlInternal -}}
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
    {{- $nubusKeycloakDefaultSubdomain := "defaultid" -}}
    {{- if .Values.ldapServer.config.samlMetadataUrl -}}
        {{- .Values.ldapServer.config.samlMetadataUrl -}}
    {{- else if and .Values.global.domain .Values.global.keycloak .Values.global.keycloak.subdomain -}}
        {{- printf "%s://%s.%s/univention/saml/metadata" $protocol .Values.global.keycloak.subdomain .Values.global.domain -}}
    {{- else if and .Values.global.nubusDeployment .Values.global.domain -}}
        {{- printf "%s://%s.%s/univention/saml/metadata" $protocol $nubusKeycloakDefaultSubdomain .Values.global.domain -}}
    {{- else -}}
        {{- required ".Values.ldapServer.config.samlServiceProviders must be defined." .Values.ldapServer.config.samlServiceProviders -}}
    {{- end -}}
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

{{- define "ldap-server.configMapUcrDefaults" -}}
    {{- $nubusDefaultConfigMapUcrDefaults := printf "%s-stack-data-ums-ucr" .Release.Name -}}
    {{- coalesce .Values.configMapUcrDefaults .Values.global.configMapUcrDefaults $nubusDefaultConfigMapUcrDefaults | required ".Values.global.configMapUcrDefaults must be defined." -}}
{{- end -}}

{{- define "ldap-server.configMapUcr" -}}
    {{- $nubusDefaultConfigMapUcr := printf "%s-stack-data-ums-ucr" .Release.Name -}}
    {{- coalesce .Values.configMapUcr .Values.global.configMapUcr $nubusDefaultConfigMapUcr -}}
{{- end -}}

{{- define "ldap-server.configMapUcrForced" -}}
    {{- coalesce .Values.configMapUcrForced .Values.global.configMapUcrForced "null" -}}
{{- end -}}

{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions releate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
They are defined so other sub-charts can read information that otherwise would be solely beknownst to this Helm chart.
If compatible Helm charts set .Values.global.nubusDeployment to true, the templates defined here will be imported.
*/}}
{{- define "nubusTemplates.ldap.protocol" -}}
ldap
{{- end -}}
{{- define "nubusTemplates.ldap.serviceName" -}}
{{- include "common.names.fullname" . -}}
{{- end -}}

{{- /*
These template definitions are only used in this chart.
*/}}
{{- define "ldap-server.samlMetadataUrl" -}}
    {{- $nubusKeycloakDefaultRealm := "nubus" -}}
    {{- $protocol := "http" -}}
    {{- $keycloakService := (printf "%s-keycloak" .Release.Name ) -}}
    {{- $keycloakServicePort := "8080" -}}
    {{- if .Values.ldapServer.config.samlMetadataUrl -}}
        {{- .Values.ldapServer.config.samlMetadataUrl -}}
    {{- else if and .Values.global.keycloak .Values.global.keycloak.realm -}}
        {{- $keycloakRealm := .Values.global.keycloak.realm -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort $keycloakRealm  -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort $nubusKeycloakDefaultRealm  -}}
    {{- else -}}
         {{- .Values.ldapServer.config.samlMetadataUrl | required ".Values.ldapServer.config.samlMetadataUrl must be defined." -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.samlMetadataUrlInternal" -}}
    {{- $nubusKeycloakDefaultRealm := "nubus" -}}
    {{- $protocol := "http" -}}
    {{- $keycloakService := (printf "%s-keycloak" .Release.Name ) -}}
    {{- $keycloakServicePort := "8080" -}}
    {{- if .Values.ldapServer.config.samlMetadataUrlInternal -}}
        {{- .Values.ldapServer.config.samlMetadataUrlInternal -}}
    {{- else if and .Values.global.keycloak .Values.global.keycloak.realm -}}
        {{- $keycloakRealm := .Values.global.keycloak.realm -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort $keycloakRealm  -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- printf "%s://%s:%s/realms/%s/protocol/saml/descriptor" $protocol $keycloakService $keycloakServicePort $nubusKeycloakDefaultRealm  -}}
    {{- else -}}
         {{- .Values.ldapServer.config.samlMetadataUrlInternal | required ".Values.ldapServer.config.samlMetadataUrlInternal must be defined." -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.samlServiceProviders" -}}
    {{- $nubusKeycloakDefaultSubdomain := "defaultid" -}}
    {{- $protocol := "https" -}}
    {{- if .Values.ldapServer.config.samlMetadataUrl -}}
        {{- .Values.ldapServer.config.samlMetadataUrl -}}
    {{- else if and .Values.global.domain .Values.global.keycloak .Values.global.keycloak.subdomain  -}}
        {{- $keycloakService := (printf "%s.%s" .Values.global.keycloak.subdomain .Values.global.domain) -}}
        {{- printf "%s://%s/univention/saml/metadata" $protocol $keycloakService -}}
    {{- else if and .Values.global.nubusDeployment .Values.global.domain -}}
        {{- $keycloakService := (printf "%s.%s" $nubusKeycloakDefaultSubdomain .Values.global.domain) -}}
        {{- printf "%s://%s/univention/saml/metadata" $protocol $keycloakService -}}
    {{- else -}}
        {{- .Values.ldapServer.config.samlServiceProviders | required ".Values.ldapServer.config.samlServiceProviders must be defined." -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.credentialSecret.name" -}}
    {{- if and .Values.ldapServer.credentialSecret .Values.ldapServer.credentialSecret.name -}}
        {{- .Values.ldapServer.credentialSecret.name -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- .Values.ldapServer.credentialSecret.name | default (printf "%s-credentials" (include "common.names.fullname" . )) -}}
    {{- else -}}
        {{- .Values.ldapServer.credentialSecret.name | required ".Values.ldapServer.credentialSecret.name must be defined." -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.credentialSecret.key" -}}
    {{- if and .Values.ldapServer.credentialSecret .Values.ldapServer.credentialSecret.key -}}
        {{- .Values.ldapServer.credentialSecret.key -}}
    {{- else if .Values.global.nubusDeployment -}}
        adminPassword
    {{- else -}}
        {{- .Values.ldapServer.credentialSecret.key | required ".Values.ldapServer.credentialSecret.key must be defined." -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.configMapUcrDefaults" -}}
    {{- $nubusDefaultConfigMapUcrDefaults := printf "%s-stack-data-ums-ucr" .Release.Name -}}
    {{- if or .Values.configMapUcrDefaults .Values.global.configMapUcrDefaults -}}
        {{- coalesce .Values.configMapUcrDefaults .Values.global.configMapUcrDefaults -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- $nubusDefaultConfigMapUcrDefaults -}}
    {{- else -}}
        {{- .Values.global.configMapUcrDefaults | required ".Values.global.configMapUcrDefaults must be defined." -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.configMapUcr" -}}
    {{- $nubusDefaultConfigMapUcr := printf "%s-stack-data-ums-ucr" .Release.Name -}}
    {{- if or .Values.configMapUcr .Values.global.configMapUcr -}}
        {{- coalesce .Values.configMapUcr .Values.global.configMapUcr -}}
    {{- else if .Values.global.nubusDeployment -}}
        {{- $nubusDefaultConfigMapUcr -}}
    {{- end -}}
{{- end -}}

{{- define "ldap-server.configMapUcrForced" -}}
    {{- if or .Values.configMapUcrForced .Values.global.configMapUcrForced -}}
        {{- coalesce .Values.configMapUcrForced .Values.global.configMapUcrForced -}}
    {{- else if .Values.global.nubusDeployment -}}
        null
    {{- end -}}
{{- end -}}

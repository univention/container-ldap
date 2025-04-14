{{- /*
SPDX-FileCopyrightText: 2024-2025 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions relate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
They are defined so other sub-charts can read information that otherwise would be solely known to this Helm chart.
If compatible Helm charts set .Values.global.nubusDeployment to true, the templates defined here will be imported.
*/}}

{{- define "nubusTemplates.ldapNotifier.connection.host" -}}
{{- printf "%s-ldap-notifier" .Release.Name -}}
{{- end -}}

{{- /*
These template definitions are only used in this chart.
*/}}

{{- define "ldap-notifier.ldapServer.volumeClaims" -}}
{{- if .Values.volumes.claims }}
{{- range $name, $claimName := .Values.volumes.claims -}}
- name: "{{ $name }}"
  persistentVolumeClaim:
    claimName: "{{ $claimName }}"
{{ end -}}
{{- else if .Values.global.nubusDeployment }}
- name: "shared-data"
  persistentVolumeClaim:
    claimName: {{ printf "shared-data-%s-ldap-server-primary-0" .Release.Name }}
- name: "shared-run"
  persistentVolumeClaim:
    claimName: {{ printf "shared-run-%s-ldap-server-primary-0" .Release.Name }}
{{- else -}}
- name: "shared-data"
  persistentVolumeClaim:
    claimName: "shared-data-ldap-server-primary-0"
- name: "shared-run"
  persistentVolumeClaim:
    claimName: "shared-run-ldap-server-primary-0"
{{- end -}}
{{- end -}}

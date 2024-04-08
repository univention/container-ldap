{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
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
    claimName: {{ printf "shared-data-%s-ldap-server-0" .Release.Name }}
- name: "shared-run"
  persistentVolumeClaim:
    claimName: {{ printf "shared-run-%s-ldap-server-0" .Release.Name }}
{{- end -}}
{{- end -}}

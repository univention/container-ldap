{{- /*
SPDX-FileCopyrightText: 2026 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- define "ldap-server.metrics.container" -}}
- name: "slapd-exporter"
  {{- if .Values.containerSecurityContext.enabled }}
  securityContext: {{- omit .Values.containerSecurityContext "enabled" | toYaml | nindent 4 }}
  {{- end }}
  image: "{{ coalesce .Values.metrics.image.registry .Values.global.imageRegistry }}/{{ .Values.metrics.image.repository }}:{{ .Values.metrics.image.tag }}"
  imagePullPolicy: {{ coalesce .Values.metrics.image.pullPolicy .Values.global.imagePullPolicy | quote }}
  args:
    - {{ printf "--uri=ldap://127.0.0.1:%v" .Values.service.ports.ldap.containerPort | quote }}
    - "--bind=simple"
    - {{ printf "--bind-dn=%s" (include "nubusTemplates.ldapServer.ldap.adminDn" .) | quote }}
    - "--bind-password-file=/var/secrets/ldap-admin/password"
    - {{ printf "--listen=:%v" .Values.metrics.containerPort | quote }}
  ports:
    - name: "metrics"
      containerPort: {{ .Values.metrics.containerPort }}
      protocol: "TCP"
  resources: {{- include "common.tplvalues.render" (dict "value" .Values.metrics.resources "context" .) | nindent 4 }}
  volumeMounts:
    - name: "metrics-bind-password"
      mountPath: "/var/secrets/ldap-admin"
      readOnly: true
{{- end -}}

{{- define "ldap-server.metrics.volume" -}}
- name: "metrics-bind-password"
  secret:
    secretName: {{ include "nubus-common.secrets.name" (dict "existingSecret" .Values.ldapServer.auth.existingSecret "defaultNameSuffix" "admin" "context" .) }}
    items:
      - key: {{ include "nubus-common.secrets.key" (dict "existingSecret" .Values.ldapServer.auth.existingSecret "key" "password" "context" .) }}
        path: "password"
{{- end -}}

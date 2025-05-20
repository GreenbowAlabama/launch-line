# templates/_helpers.tpl
{{/* Common labels */}}
{{- define "launch-lab.labels" -}}
app.kubernetes.io/name: launch-lab
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{/*
Return the name of the chart
*/}}
{{- define "launch-lab.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}
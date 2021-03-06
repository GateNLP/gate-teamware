{{/*
Expand the name of the chart.
*/}}
{{- define "gate-teamware.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 55 chars because some Kubernetes name fields are limited to 63 (by the DNS naming spec), so 55 gives us space to add "-backend".
If release name contains chart name it will be used as a full name.
*/}}
{{- define "gate-teamware.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 55 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 55 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 55 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "gate-teamware.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "gate-teamware.labels" -}}
helm.sh/chart: {{ include "gate-teamware.chart" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "gate-teamware.selectorLabels" -}}
app.kubernetes.io/name: {{ include "gate-teamware.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "gate-teamware.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "gate-teamware.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Get the name of the secret containing the superuser initial password, either a
specified existing secret or one generated by this chart.
*/}}
{{- define "gate-teamware.superuserSecret" -}}
  {{- if .Values.superuser.existingSecret -}}
    {{- .Values.superuser.existingSecret -}}
  {{- else -}}
    {{- printf "%s-superuser" (include "gate-teamware.fullname" .) -}}
  {{- end -}}
{{- end }}

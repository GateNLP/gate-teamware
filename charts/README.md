Helm Chart for Teamware
=======================

This directory contains a Helm chart to deploy GATE Teamware to a Kubernetes cluster.  The chart has been developed against Kubernetes 1.23 and may not be compatible with earlier versions, and requires Helm version 3.7 or later.

## Prerequisites

In order to run under Kubernetes there are a few prerequisites that must be satisfied first.  Most important, Kubernetes clusters cannot generally work with locally built images, so the `backend` and `static` images must be pushed to a remote Docker registry, such as Docker Hub or `ghcr.io`, and the registry name passed to helm when installing or upgrading the chart.  Secondly, the chart relies on a pair of pre-existing "secrets" in the Kubernetes namespace where the chart will be installed, holding the (ideally randomly generated) passwords for the postgresql superuser and app user, and the django `SECRET_KEY` value.  The [kubernetes-secret-generator](https://github.com/mittwald/kubernetes-secret-generator) tool is useful for this.

To set up a new installation of teamware:

- Create a suitable namespace in the cluster, and install any necessary `imagePullSecrets` - this may require additional admin privileges
- Create the random secrets described above - if your cluster has `kubernetes-secret-generator` installed then thic can be done using `kubectl create -f initial-secrets.yaml -n {namespace}`
- Create a suitable YAML file to override any defaults from `gate-teamware/values.yaml`.

Things you will commonly need to override include:

- `hostName` - set this to the fully-qualified public hostname of the teamware installation, e.g. `annotate.gate.ac.uk`
- `publicUrl` - set this to the fully qualified _public_ base URL of the site, including the protocol and port (if not 80/443) but no trailing slash.  The default is `https://{hostName}` so you should only need to override if your app is not served over HTTPS, or if it uses a non-standard port number. 
- `ingress.className` - ingress class to use, if the cluster does not have a default or if you want to use a different class from the default one.
- `ingress.tls.secret` - name of the secret holding the TLS certificate for the configured `hostName`.  Whether this is required or optional depends on the cluster and its configured ingress controller, e.g. the GATE cluster is set up to use a `*.gate.ac.uk` wildcard certificate for ingresses that do not specify their own, so on that cluster if the `hostName` matches that wildcard then a separate secret is not required.
- `email` settings to be able to send registration and password reminder emails
  - `adminAddress` - email address of the administrator, used as the "from" address on generated emails
  - `backend` - "smtp" to send mail via an SMTP server, "gmail" to use the GMail API.
  - for the "smtp" backend:
    - `host` and `port` (default 587)
    - `security` if the server requires an encrypted connection - either "tls" for STARTTLS on a regular port, or "ssl" for immediate TLS-on-connect as often used on port 465.
    - `user` and `passwordSecret` if the server requires authentication - `user` is the actual login username, `passwordSecret` is the name of a pre-existing Kubernetes secret containing a "password" key
    - `clientCertSecret` if the server requires TLS client certificate authentication.  This is the name of a standard Kubernetes "tls" type secret which contains `tls.key` and `tls.crt` entries.
  - for the "gmail" backend
    - `clientId` - the OAuth client ID for the GMail API
    - `secretName` - Kubernetes secret containing entries for "client-secret" (the OAuth client secret) and "refresh-token" (the authenticated refresh token)
- `postgresql.primary.persistence.size` (default "8Gi") - requested size for the persistent volume holding PostgreSQL data
- `postgresql.primary.persistence.storageClass` - storage class for the PostgreSQL data volume.  This is required if your cluster does not have a default StorageClass configured
  - alternatively, set `primary.persistence.existingClaim` to use an existing PVC rather than letting the StatefulSet create its own.
- `migrations.run` - set this to `true` in order to run the Django database migrations after the chart is installed.  The backend pods _do not_ run migrations at startup, as this is unsafe if there are multiple replicas or if autoscaling is in use, what this setting does is to run a one-off `Job` that just does the migrations and then exits.
- `backend.replicaCount` (default 1) - the number of replicas of the Django container to run.  Alternatively you can set `backend.autoscaling.enabled` to `true` for auto-scaling based on CPU usage
- `staticFiles.replicaCount` (default 1) - the same for the static files nginx, though this is highly unlikely to need more than one replica as it's a simple static file server
- you can also set `resources`, `nodeSelector` and/or `tolerations` if required, under both the `backend` and `staticFiles` sections

The images to be run are specified in three parts, `imageRegistry` is the registry prefix (e.g. `registry.example.com/teamware/`) which _must_ end with a slash, then `backend` and `staticFiles` have `image.repository` for the image name (default "teamware-backend" and "teamware-static" respectively) and `image.tag` for the tag, which defaults to match the chart version number, plus `pullPolicy` (default "IfNotPresent") and `pullSecrets` (if you are using a private registry whose credentials are not already configured on the default ServiceAccount for this namespace).

The chart also supports running regular backups of the database to S3 (or a compatible storage system), these can be configured using the settings under the `backup` section, see `gate-teamware/values.yaml` for more details.

## Install/upgrade

With the configured values file in place, installing or upgrading the chart uses the standard Helm command:

```
helm upgrade --install gate-teamware ./gate-teamware/ \
       --namespace {ns} --values {override-values-file}
```

e.g.

```
helm upgrade --install gate-teamware ./gate-teamware/ \
       --namespace teamware-prod --values prod-values.yaml
```

## Changelog

### Version 0.2.1

**Breaking changes**

- `postgresql.auth.existingSecret` is no longer set by default in `values.yaml`.  For new installations this means it is no longer necessary to pre-create the `postgres-credentials` secret before installing the Teamware chart, but for existing installations you must _explicitly_ set `postgresql.auth.existingSecret=postgres-credentials` in your override values when upgrading, rather than depending on that being the default setting.
- Default `imageRegistry` is now `ghcr.io/gatenlp/` - if you were previously relying on the default empty registry setting (so the deployments were just configured with `teamware-backend:{version}` and you were side-loading the images onto your cluster nodes) then you will need to set `imageRegistry: ""` in your override values when upgrading.

### Version 0.2.0

**Breaking changes**

- default postgresql database name changed from `annotations_db` to `teamware_db` - if you are upgrading an existing installation rather than installing fresh you must either:
  - explicitly override `postgresql.auth.database=annotations_db` in order to remain compatible with your existing database, or
  - ensure you have a recent backup of the database, uninstall the chart completely, delete the old postgresql PV and PVC, do a fresh install of the chart to create the database under its new name, then restore the most recent backup to the new `teamware_db` database.
    - The [postgres-restore-s3 tool](https://github.com/schickling/dockerfiles/tree/master/postgres-restore-s3) may be useful for this, but the chart cannot configure this automatically as it requires credentials that are able to _read_ from your backup bucket, and ideally the credentials provisioned for the backup CronJob should only provide _write_ access.

### Version 0.1.1

No breaking changes.

Minor changes:

- Reduced log verbosity for the static files pod by not logging k8s health check probes.

### Version 0.1.0

Initial Helm chart.



#!/bin/sh
#
# Creates a .env file with random passwords and Django secret key
#

set -e

if [ -f .env ]; then
  BAKNAME=$(date +%Y-%m-%d-%H-%M-%S)
  echo "Existing .env found - backing up as saved-env.$BAKNAME"
  cp .env saved-env.$BAKNAME
fi

# get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

case $BRANCH in 
    master|main)
        # production build
        DEPLOY_ENV=production
        MAIN_IMAGE=teamware-backend
        STATIC_IMAGE=teamware-static
        ;;
    dev)
        # staging build
        DEPLOY_ENV=staging
        MAIN_IMAGE=teamware-backend-staging
        STATIC_IMAGE=teamware-static-staging
        ;;
    *)
        # other builds, e.g. in development
        DEPLOY_ENV=development
        MAIN_IMAGE=teamware-backend-dev
        STATIC_IMAGE=teamware-static-dev
        ;;
esac

cat > .env <<EOF
PG_SUPERUSER_PASSWORD=$(openssl rand -base64 16)
DJANGO_DB_NAME=annotations_db
DB_USERNAME=gate
DB_PASSWORD=$(openssl rand -base64 16)
DJANGO_SETTINGS_MODULE=teamware.settings.deployment
DJANGO_SECRET_KEY=$(openssl rand -base64 42)
DB_BACKUP_USER=backup
DB_BACKUP_PASSWORD=$(openssl rand -base64 16)
# alter BACKUPS_VOLUME to filesystem location for db backups
BACKUPS_VOLUME=/export/raid/gate/annotations-backup-$DEPLOY_ENV
# alter BACKUPS_USER_GROUP to user id and group with permissions to write to BACKUPS_VOLUME
BACKUPS_USER_GROUP=1002:1155
DEPLOY_ENV=$DEPLOY_ENV
# If you are pushing images to a remote registry, set the registry name here
# *including* the trailing slash, e.g.
# IMAGE_REGISTRY=ghcr.io/gatenlp/
IMAGE_REGISTRY=
MAIN_IMAGE=$MAIN_IMAGE
STATIC_IMAGE=$STATIC_IMAGE
IMAGE_TAG=latest
#
# Email sending configuration
#
# For SMTP backend: django.core.mail.backends.smtp.EmailBackend
# For Gmail API backend:  gmailapi_backend.mail.GmailBackend
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# Settings for SMTP email
DJANGO_EMAIL_HOST=smtp.example.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=username
DJANGO_EMAIL_HOST_PASSWORD=password
# If the mail server requires an encrypted connection, we must specify what
# kind. Options are tls (= STARTTLS on port 25 or 587) or ssl (= "SMTPS", i.e.
# implicit TLS on connect, usually on port 465)
DJANGO_EMAIL_SECURITY=tls
# If the server requires you to identify yourself with a client certificate,
# specify it as follows:
# 
# DJANGO_EMAIL_CLIENT_KEY=/path/to/private.key
# DJANGO_EMAIL_CLIENT_CERTIFICATE=/path/to/certificate.pem
#
# The certificate file should contain the client certificate itself followed by
# any intermediate CA certificates, but not the ultimate root CA certificate


# Settings for Gmail API
DJANGO_GMAIL_API_CLIENT_ID=google_assigned_id
DJANGO_GMAIL_API_CLIENT_SECRET=google_assigned_secret
DJANGO_GMAIL_API_REFRESH_TOKEN=google_assigned_token
EOF

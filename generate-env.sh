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
BRANCH=$(git branch --show-current)

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
DJANGO_SECRET_KEY=$(openssl rand -base64 42)
DB_BACKUP_USER=backup
DB_BACKUP_PASSWORD=$(openssl rand -base64 16)
# alter BACKUPS_VOLUME to filesystem location for db backups
BACKUPS_VOLUME=/export/raid/gate/annotations-backup-$DEPLOY_ENV
DEPLOY_ENV=$DEPLOY_ENV
# If you are pushing images to a remote registry, set the registry name here
# *including* the trailing slash, e.g.
# IMAGE_REGISTRY=ghcr.io/gatenlp/
IMAGE_REGISTRY=
MAIN_IMAGE=$MAIN_IMAGE
STATIC_IMAGE=$STATIC_IMAGE
IMAGE_TAG=latest
EOF

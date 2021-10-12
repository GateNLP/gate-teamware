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
        DEPLOY_ENV=production
        MAIN_TAG=annotate-backend
        STATIC_TAG=annotate-static
        DOCKER_NETWORK=annotate-docker
        ;;
    dev)
        DEPLOY_ENV=staging
        MAIN_TAG=annotate-backend-staging
        STATIC_TAG=annotate-static-staging
        DOCKER_NETWORK=annotate-docker-staging
        ;;
    *)
        exit 1
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
BACKUPS_VOLUME=/export/raid/gate/annotations-backup-$DEPLOY_ENV
DEPLOY_ENV=$DEPLOY_ENV
MAIN_TAG=$MAIN_TAG
STATIC_TAG=$STATIC_TAG
DOCKER_NETWORK=$DOCKER_NETWORK
EOF

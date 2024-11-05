#!/bin/bash

set -e

source .env

DEPLOY_ENV=$1

case $DEPLOY_ENV in

  production|prod)
    echo "Deploying with DJANGO_ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS"
    ;;

  staging|stag)
    DJANGO_ALLOWED_HOSTS=$TEAMWARE_HOST_URL_STAGING
    export DJANGO_ALLOWED_HOSTS
    echo "Deploying with DJANGO_ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS"
    ;;

  integration)
    DJANGO_SETTINGS_MODULE=teamware.settings.docker-integration
    export DJANGO_SETTINGS_MODULE
    echo "Deploying with DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
    ;;

  *)
    exit 1
    ;;
esac

# Find a working docker compose
declare -a COMPOSE
if docker compose >/dev/null 2>&1 ; then
  # We have compose v2
  COMPOSE[0]="docker"
  COMPOSE[1]="compose"
elif which docker-compose > /dev/null 2>&1 ; then
  # We have compose v1
  COMPOSE[0]="docker-compose"
else
  echo "Could not find 'docker compose' or 'docker-compose'"
  exit 1
fi

exec "${COMPOSE[@]}" up -d

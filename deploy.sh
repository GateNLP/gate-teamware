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

docker-compose up -d

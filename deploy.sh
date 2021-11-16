#!/bin/bash

set -e

DEPLOY_ENV=$1

case $DEPLOY_ENV in

  production|prod)
    DJANGO_ALLOWED_HOSTS=annotate.gate.ac.uk
    export DJANGO_ALLOWED_HOSTS
    echo "Deploying with DJANGO_ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS"
    ;;

  staging|stag)
    DJANGO_ALLOWED_HOSTS=annotate-test.gate.ac.uk
    export DJANGO_ALLOWED_HOSTS
    echo "Deploying with DJANGO_ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS"
    ;;

  integration)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.integration
    export DJANGO_SETTINGS_MODULE
    echo "Deploying with DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
    ;;

  *)
    exit 1
    ;;
esac

docker-compose up -d

#!/bin/bash

set -e

DEPLOY_ENV=$1

case $DEPLOY_ENV in

  production|prod)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.production
    ;;

  staging|stag)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.staging
    ;;

  integration)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.integration
    ;;

  *)
    exit 1
    ;;
esac

echo "Deploying with DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE docker-compose up -d

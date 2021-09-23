#!/bin/bash

set -e

DEPLOY_ENV=$1

echo "Deploying with $DEPLOY_ENV settings"

case $DEPLOY_ENV in

  production|prod)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.production
    ;;

  staging|stag)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.staging
    ;;

  ci|testing|integration)
    DJANGO_SETTINGS_MODULE=annotation_tool.settings.integration
    ;;

  development|dev|*)
    ;;
esac

DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE docker-compose up -d

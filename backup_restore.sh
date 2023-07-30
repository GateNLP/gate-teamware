#!/bin/bash

set -e

declare -a COMPOSE
if docker compose >/dev/null 2>&1 ; then
  # We have compose v2
  COMPOSE[0]="docker"
  COMPOSE[1]="compose"
elif which docker-compose > /dev/null 2>&1 ; then
  # We have compose v1
  COMPOSE[0]="docker-compose"
else
  echo "Unable to find docker compose or docker-compose on your PATH"
  exit 1
fi

export $(grep -v '^#' .env | xargs)

# Get db container up and running
"${COMPOSE[@]}" up -d db

# Drop the schema as this is created in the backup dump
"${COMPOSE[@]}" run --rm -e DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE -e DB_USERNAME=postgres -e "DB_PASSWORD=$PG_SUPERUSER_PASSWORD" -T --entrypoint "python" backend manage.py dbshell -- -c 'DROP SCHEMA public CASCADE;'

# Run the backup restore
zcat "$1" | "${COMPOSE[@]}" run --rm -e DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE -e DB_USERNAME=postgres -e "DB_PASSWORD=$PG_SUPERUSER_PASSWORD" -T --entrypoint "python" backend manage.py dbshell --

# Reinstate the correct user permissions
"${COMPOSE[@]}" run --rm -e DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE -e DB_USERNAME=postgres -e "DB_PASSWORD=$PG_SUPERUSER_PASSWORD" -T --entrypoint "python" backend manage.py dbshell -- -c "\
GRANT ALL ON SCHEMA public TO \"$DB_USERNAME\";
GRANT ALL ON SCHEMA public TO public;
GRANT CONNECT ON DATABASE \"$DJANGO_DB_NAME\" TO \"$DB_BACKUP_USER\";
GRANT USAGE ON SCHEMA public TO \"$DB_BACKUP_USER\";\
"

# shut down the stack
"${COMPOSE[@]}" down

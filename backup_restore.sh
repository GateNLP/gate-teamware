#!/bin/bash

set -e

export $(grep -v '^#' .env | xargs)

# Get db container up and running
docker-compose up -d db

# Drop the schema as this is created in the backup dump
docker-compose run --rm -e DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE -e DB_USERNAME=postgres -e "DB_PASSWORD=$PG_SUPERUSER_PASSWORD" -T --entrypoint "python" backend manage.py dbshell -- -c 'DROP SCHEMA public CASCADE;'

# Run the backup restore
zcat "$1" | docker-compose run --rm -e DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE -e DB_USERNAME=postgres -e DB_PASSWORD=$PG_SUPERUSER_PASSWORD -T --entrypoint "python" backend manage.py dbshell --

# Reinstate the correct user permissions
docker-compose run --rm -e DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE -e DB_USERNAME=postgres -e DB_PASSWORD=$PG_SUPERUSER_PASSWORD -T --entrypoint "python" backend manage.py dbshell -- -c "\
GRANT ALL ON SCHEMA public TO \"$DB_USERNAME\";
GRANT ALL ON SCHEMA public TO public;
GRANT CONNECT ON DATABASE \"$DJANGO_DB_NAME\" TO \"$DB_BACKUP_USER\";
GRANT USAGE ON SCHEMA public TO \"$DB_BACKUP_USER\";\
"

# shut down the stack
docker-compose down

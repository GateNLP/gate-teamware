#!/bin/bash

set -e

if [ "$TEAMWARE_SKIP_SETUP" != "true" ]; then
    python manage.py makemigrations
    python manage.py migrate --no-input

    # check if database has an admin user, if not, then create one
    python manage.py check_create_superuser
fi

if [ "$TEAMWARE_ONLY_SETUP" = "true" ]; then
    exit 0
fi

exec gunicorn teamware.wsgi -b 0.0.0.0:8000 "$@"

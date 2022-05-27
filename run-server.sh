#!/bin/bash

set -e

if [ "$TEAMWARE_SKIP_SETUP" != "true" ]; then
    python manage.py makemigrations
    python manage.py migrate --no-input

    # check if database has an admin user, if not, then create one
    OUT=$(python count_superusers.py)
    echo "$OUT superusers found in database"
    if [ "$OUT" == 0 ]; then
        echo "Creating default admin user in new database..."
        echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser($SUPERUSER_USERNAME, $SUPERUSER_EMAIL, $SUPERUSER_PASSWORD)" | python manage.py shell
    fi
fi

if [ "$TEAMWARE_ONLY_SETUP" = "true" ]; then
    exit 0
fi

exec gunicorn teamware.wsgi -b 0.0.0.0:8000 "$@"

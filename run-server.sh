#!/bin/bash

set -e

# rename the secret_docker file to secret.py to use environment variables
(cd /app/annotation_tool/settings && cp secret_docker.py secret.py)

source activate annotation-tool
python manage.py makemigrations
python manage.py migrate --no-input

# check if database has an admin user, if not, then create one
OUT=$(python count_superusers.py)
echo "$OUT superusers found in database"
if [ "$OUT" == 0 ]; then
    echo "Creating default admin user in new database..."
    python manage.py loaddata --settings="$DJANGO_SETTINGS_MODULE" backend/fixtures/new_db_superuser.json
fi


gunicorn annotation_tool.wsgi -b 0.0.0.0:8000 "$@"

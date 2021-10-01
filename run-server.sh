#!/bin/bash

set -e

# rename the secret_docker file to secret.py to use environment variables
(cd /app/annotation_tool/settings && cp secret_docker.py secret.py)


DB=db.sqlite3
if test -f "$DB"; then
    chown gate:gate $DB
fi

source activate annotation-tool
python manage.py makemigrations
python manage.py migrate --no-input

su - gate --whitelist-environment=DJANGO_SETTINGS_MODULE,DJANGO_SECRET_KEY,DJANGO_DB_NAME,DB_USERNAME,DB_PASSWORD\
    --command "conda activate annotation-tool && gunicorn annotation_tool.wsgi -b 0.0.0.0:8000 $*"

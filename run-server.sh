#!/bin/bash

set -e

cp /run/secrets/django-secrets ./annotation_tool/settings/secret.py

chmod +x generate-env.sh
./generate-env.sh

source activate annotation-tool
python manage.py makemigrations
python manage.py migrate --no-input
gunicorn annotation_tool.wsgi -b 0.0.0.0:8000

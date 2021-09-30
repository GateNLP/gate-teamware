#!/bin/bash

set -e

# rename the secret_docker file to secret.py to use environment variables
(cd /app/annotation_tool/settings && mv secret_docker.py secret.py)

source activate annotation-tool
python manage.py makemigrations
python manage.py migrate --no-input
gunicorn annotation_tool.wsgi -b 0.0.0.0:8000 "$@"
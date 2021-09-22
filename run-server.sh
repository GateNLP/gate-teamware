#!/bin/bash

# su - gate --whitelist-environment=DJANGO_SETTINGS_MODULE,DJANGO_SECRET_KEY,DB_USERNAME,DB_PASSWORD\
#     --command "conda activate annotation-tool && npm run serve:docker"

set -e

cp /run/secrets/django-secrets ./annotation_tool/settings/secret.py
# chmod 777 ./annotation_tool/settings/secret.py

# chmod --recursive 777 /home/gate/
chmod +x generate-env.sh
ls -ltrh generate-env.sh
./generate-env.sh

source activate annotation-tool
# python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate --no-input
gunicorn annotation_tool.wsgi -b 0.0.0.0:8000

# conda activate annotation-tool
# npm run serve:gunicorn

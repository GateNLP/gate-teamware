#!/bin/bash

export DJANGO_SETTINGS_MODULE=annotation_tool.settings.integration

./manage.py flush --noinput &&\
./manage.py migrate --noinput &&\
./manage.py loaddata backend/fixtures/db_users.json
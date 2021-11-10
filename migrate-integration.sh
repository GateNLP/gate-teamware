#!/bin/bash

./manage.py flush --noinput --settings='annotation_tool.settings.integration' &&\
./manage.py migrate --noinput --settings='annotation_tool.settings.integration' &&\
./manage.py loaddata --settings='annotation_tool.settings.integration' backend/fixtures/db_users.json
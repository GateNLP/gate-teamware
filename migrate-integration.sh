#!/bin/bash

export DJANGO_SETTINGS_MODULE=teamware.settings.integration

./manage.py load_test_fixture "$@"

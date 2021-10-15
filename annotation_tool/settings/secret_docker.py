# "Secret" config for use in the docker container, that takes secrets from environment vars
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
POSTGRES_USERNAME = os.environ.get('DB_USERNAME')
POSTGRES_PASSWORD = os.environ.get('DB_PASSWORD')

import logging
import sys
import os
from .base import *

# Enable csrf in production
MIDDLEWARE.append(
'django.middleware.csrf.CsrfViewMiddleware'
)

if 'DJANGO_ALLOWED_HOSTS' in os.environ:
    # This looks a bit horrible, but the logic is split DJANGO_ALLOWED_HOSTS on
    # commas, strip surrounding whitespace off each element, and filter out any
    # remaining empty strings
    ALLOWED_HOSTS.extend(host for host in (h.strip() for h in os.environ['DJANGO_ALLOWED_HOSTS'].split(',')) if host)


LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'verbose': {
           'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
       },
   },
   'handlers': {
       'console': {
           'level': 'INFO',
           'class': 'logging.StreamHandler',
           'stream': sys.stdout,
           'formatter': 'verbose'
       },
   },
   'loggers': {
       '': {
           'handlers': ['console'],
           'level': 'INFO',
           'propagate': True,
       },
   },
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DJANGO_DB_NAME", "annotations_db"),
        "USER": os.environ.get("DB_USERNAME", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

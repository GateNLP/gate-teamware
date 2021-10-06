import logging
import sys
from .base import *

# Enable csrf in production
MIDDLEWARE.append(
'django.middleware.csrf.CsrfViewMiddleware'
)

ALLOWED_HOSTS.append('annotate.gate.ac.uk')


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
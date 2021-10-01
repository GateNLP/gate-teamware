from .base import *

# Enable csrf in production
MIDDLEWARE.append(
'django.middleware.csrf.CsrfViewMiddleware'
)

ALLOWED_HOSTS.append('annotate-test.gate.ac.uk')

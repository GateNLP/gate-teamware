from .base import *

# Enable csrf in production
MIDDLEWARE.append(
'django.middleware.csrf.CsrfViewMiddleware'
)


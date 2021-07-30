"""
Settings for integration testing

Uses a clean database every time
"""
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'integrationdb.sqlite3',
    }
}

# Turn off e-mail activation for testing
ACTIVATION_WITH_EMAIL = False

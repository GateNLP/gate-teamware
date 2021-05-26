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

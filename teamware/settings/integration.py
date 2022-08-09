"""
Settings for integration testing

Uses a clean database every time
"""
from .base import *

DATABASES['default']['NAME'] = "annotations_integration_db"

# Turn off e-mail activation for testing
ACTIVATION_WITH_EMAIL = False

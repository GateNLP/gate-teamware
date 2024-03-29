"""
Settings for integration testing

Uses a clean database every time
"""
from .deployment import *

DATABASES['default']['NAME'] = "teamware_integration_db"

# Turn off e-mail activation for testing
ACTIVATION_WITH_EMAIL = False

TELEMETRY_ON = False
FRONTEND_DEV_SERVER_USE = False

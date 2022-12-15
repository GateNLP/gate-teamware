"""
Settings for Dockerised CI tests
"""

from .deployment import *

TELEMETRY_ON = False
TELEMETRY_BASE_URL = 'https://127.0.0.1:8000'
TELEMETRY_PATH = 'phone_home'
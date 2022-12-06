"""
Django settings for teamware project.

The base.py file is loaded by default.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SETTINGS_DIR = Path(__file__).resolve().parent

if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = 'django-insecure-+rh5#u6=19q90g$)e%ca&wpfjsju*5*=9b#ah2b&dlwpkx%4$o'
    print("DEFAULT SECRET IS BEING USED!! This should only happen in development and automated testing")

if 'DB_USERNAME' in os.environ:
    POSTGRES_USERNAME = os.environ.get('DB_USERNAME')

if 'DB_PASSWORD' in os.environ:
    POSTGRES_PASSWORD = os.environ.get('DB_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1','0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'backend.apps.BackendConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'gmailapi_backend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'teamware.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':
            [
                os.path.join(BASE_DIR, 'templates'),
                os.path.join(BASE_DIR, 'backend/templates'),
                os.path.join(BASE_DIR, 'frontend/templates')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'teamware.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DJANGO_DB_NAME", "teamware_db"),
        "USER": os.environ.get("DB_USERNAME", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/public/static"),
    os.path.join(BASE_DIR, "frontend/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.json')
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'backend.ServiceUser'


CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

APP_NAME = "GATE Teamware"
APP_URL = os.getenv('DJANGO_APP_URL', "http://127.0.0.1:8000")

# Admin email - The mail address to be used for contacting
# users of the system
ADMIN_EMAIL = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@test.com')

# User account activation settings
ACTIVATION_URL_PATH = "/activate"
ACTIVATION_WITH_EMAIL = os.getenv('DJANGO_ACTIVATION_WITH_EMAIL', '').lower() in ['true', 'yes', 'on']
ACTIVATION_EMAIL_TIMEOUT_DAYS = 7
ACTIVATION_TOKEN_LENGTH = 128

# Password reset settings
PASSWORD_RESET_URL_PATH = "/passwordreset"
PASSWORD_RESET_TIMEOUT_HOURS = 10
PASSWORD_RESET_TOKEN_LENGTH = 128

"""
# Email Configuration - Specify e-mail backend here
# https://docs.djangoproject.com/en/3.2/topics/email/
# django-gmailapi-backend (https://github.com/dolfim/django-gmailapi-backend) is used for sending
# emails though Google's API. See documentation for more details.
"""

"""
Select the email backend to use
Emails are sent to local memory by default: django.core.mail.backends.locmem.EmailBackend
For SMTP: django.core.mail.backends.smtp.EmailBackend
For Gmail tokens: gmailapi_backend.mail.GmailBackend

"""
EMAIL_BACKEND = os.getenv('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.locmem.EmailBackend')

"""
Send e-mail through standard SMTP server. See [https://github.com/dolfim/django-gmailapi-backend](https://github.com/dolfim/django-gmailapi-backend)
for full list of configuration parameters.
"""
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('DJANGO_EMAIL_PORT', 25))
if 'DJANGO_EMAIL_HOST_USER' in os.environ:
    # If user is set then password must also, and we want to raise an
    # exception if it's missing
    EMAIL_HOST_USER = os.environ['DJANGO_EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['DJANGO_EMAIL_HOST_PASSWORD']

if 'DJANGO_EMAIL_SECURITY' in os.environ:
    if os.environ['DJANGO_EMAIL_SECURITY'].lower() == 'ssl':
        EMAIL_USE_SSL = True
    elif os.environ['DJANGO_EMAIL_SECURITY'].lower() == 'tls':
        EMAIL_USE_TLS = True
    else:
        raise ValueError("DJANGO_EMAIL_SECURITY, if set, must be either SSL or TLS")

    if 'DJANGO_EMAIL_CLIENT_CERTIFICATE' in os.environ:
        # If certificate is set then key must also, and we want to raise an
        # exception if it's missing
        EMAIL_SSL_CERTFILE = os.environ['DJANGO_EMAIL_CLIENT_CERTIFICATE']
        EMAIL_SSL_KEYFILE = os.environ['DJANGO_EMAIL_CLIENT_KEY']

"""
If sending e-mail through Gmail using Google's API, the following parameters must be set:
"""
GMAIL_API_CLIENT_ID = os.getenv('DJANGO_GMAIL_API_CLIENT_ID', 'google_assigned_id')
GMAIL_API_CLIENT_SECRET = os.getenv('DJANGO_GMAIL_API_CLIENT_SECRET', 'google_assigned_secret')
GMAIL_API_REFRESH_TOKEN = os.getenv('DJANGO_GMAIL_API_REFRESH_TOKEN', 'google_assigned_token')




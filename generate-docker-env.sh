#!/bin/bash
#
# Creates a .env file with random passwords and Django secret key

set -e

if [ -f .env ]; then
  BAKNAME=$(date +%Y-%m-%d-%H-%M-%S)
  echo "Existing .env found - backing up as saved-env.$BAKNAME"
  cp .env saved-env.$BAKNAME

  # load any existing environment variables from .env
  . .env
   sed -n '/^### generate-docker-env\.sh will not touch anything below this line/,$p' .env | sed 1d > .env.tmpsave
fi

# get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

case $BRANCH in 
    master|main)
        # production build
        DEPLOY_ENV=production
        MAIN_IMAGE=${MAIN_IMAGE:-teamware-backend}
        STATIC_IMAGE=${STATIC_IMAGE:-teamware-static}
        ;;
    dev)
        # staging build
        DEPLOY_ENV=staging
        MAIN_IMAGE=${MAIN_IMAGE:-teamware-backend-staging}
        STATIC_IMAGE=${STATIC_IMAGE:-teamware-static-staging}
        ;;
    *)
        # other builds, e.g. in development
        DEPLOY_ENV=development
        MAIN_IMAGE=${MAIN_IMAGE:-teamware-backend-dev}
        STATIC_IMAGE=${STATIC_IMAGE:-teamware-static-dev}
        ;;
esac

# Populate .env with either existing or default values of the environment variables
cat > .env <<EOF
# GATE Teamware Docker Deployment Configuration
# Add values to the variables here, most existing values will be kept after running generate-docker-env.sh
# Anything that is left blank will be filled with a default value.
# Passwords and keys are filled with auto-generated random values.
# If you want to add any *new* variables - those must be added at the bottom after the DO NOT EDIT line

# Database details
PG_SUPERUSER_PASSWORD=${PG_SUPERUSER_PASSWORD:-$(openssl rand -base64 16)} # default: auto-generated
DJANGO_DB_NAME=${DJANGO_DB_NAME:-annotations_db}
DB_USERNAME=${DB_USERNAME:-gate}
DB_PASSWORD=${DB_PASSWORD:-$(openssl rand -base64 16)} # default: auto-generated

# Django settings
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-teamware.settings.deployment}
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-$(openssl rand -base64 42)} # default: auto-generated


# Database backup user credentials
DB_BACKUP_USER=${DB_BACKUP_USER:-backup}
DB_BACKUP_PASSWORD=${DB_BACKUP_PASSWORD:-$(openssl rand -base64 16)} # default: auto-generated

# Path to backup location
BACKUPS_VOLUME=${BACKUPS_VOLUME:-/var/lib/teamware-backup/}

# User permissions for the backup user on the host filesystem (user:group)
BACKUPS_USER_GROUP=${BACKUPS_USER_GROUP:-0:0}

# Set automatically as production, staging or development based on branch (master, dev, other)
DEPLOY_ENV=$DEPLOY_ENV

# Default credentials user for setting up database
# Only used if no superusers are found in database
SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-gate+teamware@sheffield.ac.uk}
SUPERUSER_USERNAME=${SUPERUSER_USERNAME:-admin}
SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:-password}

#
# If you are pushing images to a remote registry, set the registry names here
# *including* the trailing slash
#
IMAGE_REGISTRY=${IMAGE_REGISTRY:-ghcr.io/gatenlp/} # leave blank for local images
MAIN_IMAGE=$MAIN_IMAGE # Do not change
STATIC_IMAGE=$STATIC_IMAGE # Do not change
IMAGE_TAG=${IMAGE_TAG:-latest}

#
# Email sending configuration
#
# For SMTP backend: django.core.mail.backends.smtp.EmailBackend
# For Gmail API backend:  gmailapi_backend.mail.GmailBackend
DJANGO_EMAIL_BACKEND=${DJANGO_EMAIL_BACKEND:-django.core.mail.backends.smtp.EmailBackend}

# Settings for Gmail API
DJANGO_GMAIL_API_CLIENT_ID=${DJANGO_GMAIL_API_CLIENT_ID:-google_assigned_id}
DJANGO_GMAIL_API_CLIENT_SECRET=${DJANGO_GMAIL_API_CLIENT_SECRET:-google_assigned_secret}
DJANGO_GMAIL_API_REFRESH_TOKEN=${DJANGO_GMAIL_API_REFRESH_TOKEN:-google_assigned_token}

# Settings for SMTP email
DJANGO_EMAIL_HOST=${DJANGO_EMAIL_HOST:-smtp.example.com}
DJANGO_EMAIL_PORT=${DJANGO_EMAIL_PORT:-587}
DJANGO_EMAIL_HOST_USER=${DJANGO_EMAIL_HOST_USER:-username}
DJANGO_EMAIL_HOST_PASSWORD=${DJANGO_EMAIL_HOST_PASSWORD:-password}

# If the mail server requires an encrypted connection, we must specify what
# kind. Options are tls (= STARTTLS on port 25 or 587) or ssl (= "SMTPS", i.e.
# implicit TLS on connect, usually on port 465)
DJANGO_EMAIL_SECURITY=${DJANGO_EMAIL_SECURITY:-tls}

# If the server requires you to identify yourself with a client certificate,
# Add these variables at the bottom of this file, after the DO NOT EDIT line
# 
# DJANGO_EMAIL_CLIENT_KEY=/path/to/private.key
# DJANGO_EMAIL_CLIENT_CERTIFICATE=-/path/to/certificate.pem

### DO NOT EDIT THIS COMMENT
### generate-docker-env.sh will not touch anything below this line
EOF

if [ -f .env.tmpsave ]; then
  cat .env.tmpsave >> .env
  rm .env.tmpsave
fi

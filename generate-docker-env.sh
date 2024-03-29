#!/bin/bash
#
# Creates a .env file with random passwords and Django secret key

function quote_string {
  if [ -n "$1" ]; then
    local QUOTED=${1//\\/\\\\}
    QUOTED=${QUOTED//\"/\\\"}
    QUOTED=${QUOTED//\$/\$\{__DOLLAR__\}}
    QUOTED=${QUOTED//\`/\$\{__BT__\}}
    printf '"%s"' "${QUOTED}"
  fi
}

set -e

if [ -f .env ]; then
  BAKNAME=$(date +%Y-%m-%d-%H-%M-%S)
  echo "Existing .env found - backing up as saved-env.$BAKNAME"
  cp .env saved-env.$BAKNAME

  # load any existing environment variables from .env
  if [ -z "$SKIP_EXISTING_ENV" ]; then
    . .env
  fi
   sed -n '/^### generate-docker-env\.sh will not touch anything below this line/,$p' .env | sed 1d > .env.tmpsave
fi

# get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)

case $BRANCH in 
    master|main)
        # production build
        MAIN_IMAGE=${MAIN_IMAGE:-teamware-backend}
        STATIC_IMAGE=${STATIC_IMAGE:-teamware-static}
        ;;
    dev)
        # staging build
        MAIN_IMAGE=${MAIN_IMAGE:-teamware-backend-staging}
        STATIC_IMAGE=${STATIC_IMAGE:-teamware-static-staging}
        ;;
    *)
        # other builds, e.g. in development
        MAIN_IMAGE=${MAIN_IMAGE:-teamware-backend-dev}
        STATIC_IMAGE=${STATIC_IMAGE:-teamware-static-dev}
        ;;
esac

# If backups directory exists but user/group is not set, set it to match the
# actual ownership of the directory
if [ -d "${BACKUPS_VOLUME:=./backups/}" ]; then
  if [ -z "$BACKUPS_USER_GROUP" ]; then
    # stat -c works with GNU stat, stat -f is the equivalent in BSD stat (e.g. Mac OS).
    # If neither of these work then the variable will be left empty and will be
    # defaulted to 0:0
    BACKUPS_USER_GROUP=`stat -c '%u:%g' "$BACKUPS_VOLUME" 2>/dev/null || stat -f '%u:%g' "$BACKUPS_VOLUME" 2>/dev/null`
  fi
fi

# Populate .env with either existing or default values of the environment variables
exec 3> .env

cat 1>&3 <<EOF
# GATE Teamware Docker Deployment Configuration
# Add values to the variables here, most existing values will be kept after running generate-docker-env.sh
# Anything that is left blank will be filled with a default value.
# Passwords and keys are filled with auto-generated random values.
# If you want to add any *new* variables - those must be added at the bottom after the DO NOT EDIT line

# These variables are a trick to ensure that bash, "docker compose" (v2) and "docker-compose" (v1) all
# interpret this file the same way.  If you edit any of these variables and want to include a backtick
# character (\`) in the value, you must represent it as \${__BT__}, and dollar (\$) as \${__DOLLAR__}
__BT__='\`'
__DOLLAR__='$'

# Database details
PG_SUPERUSER_PASSWORD=`quote_string "${PG_SUPERUSER_PASSWORD:-$(openssl rand -base64 16)}"` # default: auto-generated
DJANGO_DB_NAME=${DJANGO_DB_NAME:-teamware_db}
DB_USERNAME=${DB_USERNAME:-gate}
DB_PASSWORD=`quote_string "${DB_PASSWORD:-$(openssl rand -base64 16)}"` # default: auto-generated

# Django settings
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-teamware.settings.deployment}
DJANGO_SECRET_KEY=`quote_string "${DJANGO_SECRET_KEY:-$(openssl rand -base64 42)}"` # default: auto-generated

# Allowed host urls - DJANGO_ALLOWED_HOSTS for production deployment,
# TEAMWARE_HOST_URL_STAGING overrides this for staging deployment
DJANGO_ALLOWED_HOSTS=`quote_string "${DJANGO_ALLOWED_HOSTS:-$TEAMWARE_HOST_URL_PRODUCTION}"`
TEAMWARE_HOST_URL_STAGING=`quote_string "${TEAMWARE_HOST_URL_STAGING}"`

# Public app URL, used to build links in activation emails
DJANGO_APP_URL=`quote_string "${DJANGO_APP_URL:-http://${DJANGO_ALLOWED_HOSTS:-localhost}:8076}"`

# Database backup user credentials
DB_BACKUP_USER=${DB_BACKUP_USER:-backup}
DB_BACKUP_PASSWORD=`quote_string "${DB_BACKUP_PASSWORD:-$(openssl rand -base64 16)}"` # default: auto-generated

# Path to backup location
BACKUPS_VOLUME=`quote_string "${BACKUPS_VOLUME}"`

# User permissions for the backup user on the host filesystem (user:group)
BACKUPS_USER_GROUP=${BACKUPS_USER_GROUP:-0:0}

# Default credentials user for setting up database
# Only used if no superusers are found in database
SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-teamware@example.com}
SUPERUSER_USERNAME=${SUPERUSER_USERNAME:-admin}
SUPERUSER_PASSWORD=`quote_string "${SUPERUSER_PASSWORD:-password}"`

#
# If you are pushing images to a remote registry, set the registry names here
# *including* the trailing slash
#
# leave blank for local images
IMAGE_REGISTRY=${IMAGE_REGISTRY-ghcr.io/gatenlp/}
MAIN_IMAGE=$MAIN_IMAGE # Do not change
STATIC_IMAGE=$STATIC_IMAGE # Do not change
IMAGE_TAG=${IMAGE_TAG:-latest}

# Require email activation for new user accounts?
DJANGO_ACTIVATION_WITH_EMAIL=${DJANGO_ACTIVATION_WITH_EMAIL:-no}

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
DJANGO_EMAIL_HOST_USER=${DJANGO_EMAIL_HOST_USER-username}
DJANGO_EMAIL_HOST_PASSWORD=`quote_string "${DJANGO_EMAIL_HOST_PASSWORD-password}"`

# If the mail server requires an encrypted connection, we must specify what
# kind. Options are tls (= STARTTLS on port 25 or 587) or ssl (= "SMTPS", i.e.
# implicit TLS on connect, usually on port 465)
DJANGO_EMAIL_SECURITY=${DJANGO_EMAIL_SECURITY-tls}

# If the server requires you to identify yourself with a client certificate,
# Add these variables at the bottom of this file, after the DO NOT EDIT line
#
# DJANGO_EMAIL_CLIENT_KEY=/path/to/private.key
# DJANGO_EMAIL_CLIENT_CERTIFICATE=/path/to/certificate.pem

# Privacy Policy and T&C Details
PP_HOST_NAME=`quote_string "${PP_HOST_NAME:-GATE}"`
PP_HOST_ADDRESS=`quote_string "${PP_HOST_ADDRESS:-Department of Computer Science, The University of Sheffield, Regent Court, 211 Portobello, Sheffield, S1 4DP. UK}"`
PP_HOST_CONTACT=`quote_string "${PP_HOST_CONTACT:-<a href='https://gate.ac.uk/g8/contact' target='_blank'>Contact GATE</a>}"`

# If admin (responsible for managing users) is not the same as the host
# (who manages the underlying server) then set their details separately
EOF

if [ -n "$PP_ADMIN_NAME" ]; then
  echo "PP_ADMIN_NAME=$(quote_string "${PP_ADMIN_NAME}")" 1>&3
else
  echo "# PP_ADMIN_NAME=\"Administrator's name\"" 1>&3
fi

if [ -n "$PP_ADMIN_ADDRESS" ]; then
  echo "PP_ADMIN_ADDRESS=$(quote_string "${PP_ADMIN_ADDRESS}")" 1>&3
else
  echo "# PP_ADMIN_ADDRESS=\"123 Anywhere Street, Sometown\"" 1>&3
fi

if [ -n "$PP_ADMIN_CONTACT" ]; then
  echo "PP_ADMIN_CONTACT=$(quote_string "${PP_ADMIN_CONTACT}")" 1>&3
else
  echo "# PP_ADMIN_CONTACT=\"<a href='mailto:admin@example.com'>Contact the admin</a>\"" 1>&3
fi

cat 1>&3 <<EOF

### DO NOT EDIT THIS COMMENT
### generate-docker-env.sh will not touch anything below this line
EOF

if [ -f .env.tmpsave ]; then
  cat .env.tmpsave >> .env
  rm .env.tmpsave
fi

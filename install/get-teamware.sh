#!/bin/bash
#
# This is a quick-start script that will download the minimal files required
# to deploy GATE Teamware using docker compose, prompt the user for the
# necessary configuration options and create an initial .env file
#

# GATE Teamware version that this script will install
DEFAULT_IMAGE_TAG=latest

export MAIN_IMAGE=teamware-backend
export STATIC_IMAGE=teamware-static
export IMAGE_TAG=${IMAGE_TAG-$DEFAULT_IMAGE_TAG}

# Locate docker
if which docker > /dev/null 2>&1 ; then
  DOCKER=docker
else
  echo '"docker" command is not available on your PATH!'
  while [ -z "$DOCKER" -o ! -x "$DOCKER" ]; do
    read -e -p "Enter full path to docker: " DOCKER
  done
fi

# Find a working docker compose
declare -a COMPOSE
if "$DOCKER" compose >/dev/null 2>&1 ; then
  # We have compose v2
  COMPOSE[0]="$DOCKER"
  COMPOSE[1]="compose"
elif which docker-compose > /dev/null 2>&1 ; then
  # We have compose v1
  COMPOSE[0]="docker-compose"
else
  echo '"docker compose" not available, and "docker-compose" not found on your PATH.'
  while [ -z "$DOCKER_COMPOSE" -o ! -x "$DOCKER_COMPOSE" ]; do
    read -e -p "Enter full path to docker-compose: " DOCKER_COMPOSE
  done
  COMPOSE[0]="${DOCKER_COMPOSE}"
fi

# Find a working curl
declare -a CURL
if which curl >/dev/null 2>&1 ; then
  CURL=("curl" "-L")
elif which wget >/dev/null 2>&1 ; then
  CURL=("wget" "-O" "-")
else
  # Can't find curl, but we do have Docker so we can run curl via docker
  CURL=("$DOCKER" "run" "--rm" "curlimages/curl" "-L")
fi

# Gather information for env file
set -a

if [ -f .env -a -f docker-compose.yml ]; then

  if ! [ -f create-django-db.sh -a -f generate-docker-env.sh ]; then
    echo 'You have run this upgrade script in a folder that contains a docker compose'
    echo 'application stack, but it does not appear to be an installation of GATE'
    echo 'Teamware.  You should run this script either in a completely empty directory'
    echo 'if you want to install a fresh copy of GATE Teamware, or in the directory'
    echo 'containing an existing installation that you want to upgrade.  Running in'
    echo 'a directory that contains a different docker compose application stack will'
    echo 'not work and may cause damage or data loss.'
    echo ''
    read -e -p 'Do you wish to continue anyway? [y/N]: ' CONTINUE_UPGRADE
    case "$CONTINUE_UPGRADE" in
      [Yy]*)
        unset CONTINUE_UPGRADE
        ;;
      *)
        exit 1
        ;;
    esac
  fi

  echo 'Existing settings found, assuming this is an upgrade.'
  NEW__IMAGE_TAG="${IMAGE_TAG}"
  . .env
  OLD__IMAGE_TAG="${IMAGE_TAG}"
  IMAGE_TAG="${NEW__IMAGE_TAG}"
  if [ "${OLD__IMAGE_TAG}" = "${NEW__IMAGE_TAG}" ]; then
    echo "This is the installation script for ${NEW__IMAGE_TAG}, but you already have this version."
    read -e -p 'Do you wish to continue? [y/N]: ' CONTINUE_UPGRADE
    case "$CONTINUE_UPGRADE" in
      [Yy]*)
        ;;
      *)
        exit 1
        ;;
    esac
  else
    echo "Upgrading from ${OLD__IMAGE_TAG} to ${IMAGE_TAG}"
  fi
fi

OLD__DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS:-localhost}
echo 'GATE Teamware needs to know the public host name at which it will be accessed'
echo 'by users - only connections to that host name or "localhost" are accepted.'
read -e -p "Public hostname of GATE Teamware [default $OLD__DJANGO_ALLOWED_HOSTS]: " DJANGO_ALLOWED_HOSTS
if [ -z "$DJANGO_ALLOWED_HOSTS" ]; then
  DJANGO_ALLOWED_HOSTS=${OLD__DJANGO_ALLOWED_HOSTS}
fi

DEFAULT__IS_HTTPS=Y
case "$DJANGO_APP_URL" in
  http:*)
    DEFAULT__IS_HTTPS=N
    ;;
esac

read -e -p "Will users connect to GATE Teamware via https? (default ${DEFAULT__IS_HTTPS}): " IS_HTTPS
if [ -z "$IS_HTTPS" ]; then
  IS_HTTPS=$DEFAULT__IS_HTTPS
fi

case $IS_HTTPS in
  [Nn]*)
    unset IS_HTTPS
    ;;
  *)
    DJANGO_APP_URL=https://${DJANGO_ALLOWED_HOSTS}
    ;;
esac

if [ -z "$SUPERUSER_EMAIL" ]; then
  read -e -p 'Email address of initial "admin" user [default "teamware@example.com"]: ' SUPERUSER_EMAIL
  read -e -p 'Initial password for "admin" user [default "password"]: ' SUPERUSER_PASSWORD
fi

echo ''
if [ "$DJANGO_EMAIL_BACKEND" = "gmailapi_backend.mail.GmailBackend" ]; then
  echo "GATE Teamware is currently configured to send email using the Gmail API,"
  echo "these settings cannot be modified here, you should edit the .env file"
  echo "yourself later."
else
  if [ -n "$DJANGO_EMAIL_HOST" ]; then
    echo "Current outgoing email server settings:"
    echo "Hostname: ${DJANGO_EMAIL_HOST}"
    echo "Port: ${DJANGO_EMAIL_PORT}"
    if [ -n "${DJANGO_EMAIL_HOST_USER}" ]; then
      echo "Username: ${DJANGO_EMAIL_HOST_USER}"
    fi
    if [ -n "${DJANGO_EMAIL_HOST_PASSWORD}" ]; then
      echo "Password: <hidden>"
    fi
    case "${DJANGO_EMAIL_SECURITY}" in
      ssl|tls)
        echo "Secure connection: Y"
        ;;
      *)
        echo "Secure connection: N"
        ;;
    esac
    echo ""
    read -p "Change these settings? (y/N): " EDIT_EMAIL_SETTINGS
    case "$EDIT_EMAIL_SETTINGS" in
      [yY]*)
        unset DJANGO_EMAIL_HOST
      ;;
    esac
  fi

  if [ -z "$DJANGO_EMAIL_HOST" ]; then
    echo 'GATE Teamware needs to be able to send outgoing email for password resets, etc.'
    echo 'You can configure an SMTP server here, or edit your settings later to use the'
    echo 'GMail API.'
    read -e -p 'SMTP server hostname: ' DJANGO_EMAIL_HOST
    read -e -p 'SMTP server port number [default 587, may be 25 or 465]: ' DJANGO_EMAIL_PORT
    read -e -p 'SMTP server username, if required: ' DJANGO_EMAIL_HOST_USER
    read -e -s -p 'SMTP server password, if required: ' DJANGO_EMAIL_HOST_PASSWORD
    echo "" # read -s doesn't add a line break
    read -e -p 'Does SMTP server require a secure connection? [Y/n]: ' EMAIL_SECURE

    case "$EMAIL_SECURE" in
      [Nn]*)
        DJANGO_EMAIL_SECURITY=
        ;;

      *)
        if [ "$DJANGO_EMAIL_PORT" = "465" ]; then
          DJANGO_EMAIL_SECURITY=ssl
        else
          DJANGO_EMAIL_SECURITY=tls
        fi
        ;;
    esac
  fi
fi

echo 'Privacy policy / Terms & conditions'
echo ''
echo 'GATE Teamware includes a standard privacy policy and T&C document intended'
echo 'to be suitable for an installation governed by English law.  To use these'
echo 'standard documents you must provide the legal name, address and contact'
echo 'method for the person or organisation responsible for this installation.'
echo 'If the default policies are not suitable for your needs you will need to'
echo 'create your own and save them in the "custom-policies" folder as Markdown.'
echo 'See the template files in that folder for more details.'
echo ''

if [ -n "$PP_HOST_NAME" ]; then
  echo 'Current settings for privacy policy and terms:'
  echo "Legal name of the entity responsible for this Teamware: $PP_HOST_NAME"
  echo "Physical address of this entity: $PP_HOST_ADDRESS"
  echo "Contact link: $PP_HOST_CONTACT"
  echo ""
  read -p "Change these settings? (y/N): " EDIT_PP_SETTINGS
  case "$EDIT_PP_SETTINGS" in
    [yY]*)
      unset PP_HOST_NAME
    ;;
  esac
fi

if [ -z "$PP_HOST_NAME" ]; then
  read -e -p 'Legal name of the entity responsible for this Teamware: ' PP_HOST_NAME
  read -e -p 'Physical address of this entity: ' PP_HOST_ADDRESS
  read -e -p 'Contact email address or web URL (including http(s)://) for the host: ' PP_HOST_EMAIL_OR_URL

  if [ "${PP_HOST_EMAIL_OR_URL#http://}" != "$PP_HOST_EMAIL_OR_URL" ] || [ "${PP_HOST_EMAIL_OR_URL#https://}" != "$PP_HOST_EMAIL_OR_URL" ]; then
    # it's a URL
    PP_HOST_CONTACT="<a href='${PP_HOST_EMAIL_OR_URL}'>Contact $PP_HOST_NAME</a>"
  else
    # assume it's an email
    PP_HOST_CONTACT="<a href='mailto:${PP_HOST_EMAIL_OR_URL}'>Email $PP_HOST_NAME</a>"
  fi
fi

echo ''
echo 'GATE Teamware normally requires new users to confirm their email address'
echo 'by clicking a link in an activation email.  If you are just testing GATE'
echo 'Teamware locally you may wish to disable this so new accounts are active'
echo 'immediately.'
case "${DJANGO_ACTIVATION_WITH_EMAIL:-yes}" in
  [Tt][Rr][Uu][Ee]|[Yy][Ee][Ss]|[Oo][Nn])
    DEFAULT__EMAIL_ACTIVATION=y
    ;;

  *)
    DEFAULT__EMAIL_ACTIVATION=n
    ;;
esac
read -e -p "Require new users to confirm their email address? [y/n, default $DEFAULT__EMAIL_ACTIVATION]: " EMAIL_ACTIVATION

case "${EMAIL_ACTIVATION:-$DEFAULT__EMAIL_ACTIVATION}" in
  [Nn]*)
    DJANGO_ACTIVATION_WITH_EMAIL=no
    ;;

  *)
    DJANGO_ACTIVATION_WITH_EMAIL=yes
    ;;
esac

set +a

# Download install package
if [ "$IMAGE_TAG" = "latest" -o "$IMAGE_TAG" = "dev" ]; then
  "${CURL[@]}" https://github.com/GateNLP/gate-teamware/releases/latest/download/install.tar.gz > install.tar.gz
else
  "${CURL[@]}" https://github.com/GateNLP/gate-teamware/releases/download/v${IMAGE_TAG}/install.tar.gz > install.tar.gz
fi

# Back up any files that would be overwritten when unpacking the tar.gz - there
# is an option that will do this automatically in GNU tar but it doesn't work
# with the BSD tar in Mac OS X
tar tzf install.tar.gz | while read FILENAME ; do
  if [ -f "$FILENAME" ]; then
    cp "$FILENAME" "$FILENAME.bak"
  fi
done

# Now unpack the archive
tar xzf install.tar.gz

# Create backup folder
mkdir -p backups

# Double check permissions on the files that will be bind-mounted
chmod 755 nginx create-django-db.sh custom-policies
chmod 644 nginx/*.template Caddyfile

echo "Generating configuration file"

# tell generate-docker-env not to load an existing .env itself, since we already have
SKIP_EXISTING_ENV=yes
source ./generate-docker-env.sh

if [ "${COMPOSE[0]/ /_}" = "${COMPOSE[0]}" ]; then
  # docker or compose path does not contain any spaces
  COMPOSE_CMDLINE="${COMPOSE[*]}"
else
  # path to docker contains spaces, so must be quoted
  COMPOSE_CMDLINE="\"${COMPOSE[0]}\" ${COMPOSE[*]:1}"
fi

cat <<EOF

Your GATE Teamware installation is ready to use, your configuration has been
written to the file ".env", which you can edit as required.

To start up GATE Teamware for local experimentation, run:

  $COMPOSE_CMDLINE up -d

By default the application is accessible at http://localhost:8076 - to change
the port number you will need to edit docker-compose.yml.

EOF

if [ "$DJANGO_ALLOWED_HOSTS" = "localhost" ]; then
  cat <<EOF
You can use

  $COMPOSE_CMDLINE -f docker-compose.yml -f docker-compose-https.yml up -d

to include a simple HTTPS reverse proxy server that uses a locally-generated
certificate - for production use you should edit DJANGO_ALLOWED_HOSTS and
DJANGO_APP_URL in your .env file and set up a proper reverse proxy.
EOF
else
  cat <<EOF
Public access should be via HTTPS.  If the host where you are running Teamware
is directly accessible from the internet at

  https://$DJANGO_ALLOWED_HOSTS

then you can use

  $COMPOSE_CMDLINE -f docker-compose.yml -f docker-compose-https.yml up -d

to include a simple HTTPS reverse proxy server that obtains certificates from
LetsEncrypt.  If this host is not internet-accessible you will need to set up
your own reverse proxy server elsewhere.
EOF
fi

if [ -n "$NEW__IMAGE_TAG" ]; then
  echo ""
  echo "Existing files that were part of your previous version of GATE Teamware"
  echo "have been backed up with a .bak extension. If you have made any modifications"
  echo "to any of these files since you originally installed GATE Teamware (for"
  echo "example to change the public port number in docker-compose.yml) then you"
  echo "will need to compare the backup files to their new versions and make the"
  echo "appropriate changes yourself."
fi

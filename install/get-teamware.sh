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
echo 'GATE Teamware needs to know the public host name at which it will be accessed'
echo 'by users - only connections to that host name or "localhost" are accepted.'
read -e -p 'Public hostname of GATE Teamware (e.g. teamware.example.com): ' DJANGO_ALLOWED_HOSTS
read -e -p 'Email address of initial "admin" user [default "teamware@example.com"]: ' SUPERUSER_EMAIL
read -e -p 'Initial password for "admin" user [default "password"]: ' SUPERUSER_PASSWORD

echo ''
echo 'GATE Teamware needs to be able to send outgoing email for user registration,'
echo 'password resets, etc.  You can configure an SMTP server here, or edit your'
echo 'settings later to use the GMail API.'
read -e -p 'SMTP server hostname: ' DJANGO_EMAIL_HOST
read -e -p 'SMTP server port number [default 587, may be 25 or 465]: ' DJANGO_EMAIL_PORT
read -e -p 'SMTP server username, if required: ' DJANGO_EMAIL_HOST_USER
read -e -s -p 'SMTP server password, if required: ' DJANGO_EMAIL_HOST_PASSWORD
echo "" # read -s doesn't add a line break
read -e -p 'Does SMTP server require a secure connection? [Y/n]: ' EMAIL_SECURE

case $EMAIL_SECURE in
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

set +a

# Download install package
if [ "$IMAGE_TAG" = "latest" -o "$IMAGE_TAG" = "dev" ]; then
  "${CURL[@]}" https://github.com/GateNLP/gate-teamware/releases/latest/download/install.tar.gz | tar xzf -
else
  "${CURL[@]}" https://github.com/GateNLP/gate-teamware/releases/download/v${IMAGE_TAG}/install.tar.gz | tar xzf -
fi

# Create backup folder
mkdir backups

# Double check permissions on the files that will be bind-mounted
chmod 755 nginx create-django-db.sh custom-policies
chmod 644 nginx/*.template

echo "Generating configuration file"

source ./generate-docker-env.sh

cat <<EOF

Your GATE Teamware installation is ready to use, your configuration has been
written to the file ".env", which you can edit as required.

To start up GATE Teamware, run:

EOF
if [ "${COMPOSE[0]/ /_}" = "${COMPOSE[0]}" ]; then
  # docker or compose path does not contain any spaces
  echo "${COMPOSE[*]} up -d"
else
  # path to docker contains spaces, so must be quoted
  echo "\"${COMPOSE[0]}\" ${COMPOSE[*]:1} up -d"
fi

cat <<EOF

By default the application is accessible at http://localhost:8076 - to change
the port number you will need to edit docker-compose.yml.  We strongly
recommend that public access be via secure HTTPS, for which you will need
to deploy a separate front end proxy forwarding to the GATE Teamware
application; configuration of such a proxy is beyond the scope of this quick
start script.
EOF

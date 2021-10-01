#!/bin/sh
#
# Creates a .env file with random passwords and Django secret key
#

if [ -f .env ]; then
  BAKNAME=$(date +%Y-%m-%d-%H-%M-%S)
  echo "Existing .env found - backing up as saved-env.$BAKNAME"
  cp .env saved-env.$BAKNAME
fi

cat > .env <<EOF
PG_SUPERUSER_PASSWORD=$(openssl rand -base64 16)
DJANGO_DB_NAME=annotations_db
DB_USERNAME=gate
DB_PASSWORD=$(openssl rand -base64 16)
DJANGO_SECRET_KEY=$(openssl rand -base64 42)
DB_BACKUP_USER=backup
DB_BACKUP_PASSWORD=$(openssl rand -base64 16)
EOF

#!/bin/bash

set -e

declare -a COMPOSE
if docker compose >/dev/null 2>&1 ; then
  # We have compose v2
  COMPOSE[0]="docker"
  COMPOSE[1]="compose"
elif which docker-compose > /dev/null 2>&1 ; then
  # We have compose v1
  COMPOSE[0]="docker-compose"
else
  echo "Unable to find docker compose or docker-compose on your PATH"
  exit 1
fi

"${COMPOSE[@]}" run --rm -it pgbackups /backup.sh
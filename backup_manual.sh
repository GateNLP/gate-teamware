#!/bin/bash

set -e

docker-compose run --rm --entrypoint="/bin/bash" pgbackups ./backup.sh
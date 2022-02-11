#!/bin/bash

set -e

docker-compose run --rm -e --entrypoint="/bin/bash" pgbackups ./backup.sh
#!/bin/sh
#
# Run Django migrations against the postgresql container to create the initial
# schema or migrate after an upgrade
#

docker-compose run --rm --entrypoint "python" backend manage.py migrate

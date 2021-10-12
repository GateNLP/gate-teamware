#!/bin/bash

set -e

# set environment variables from file
set -o allexport
source .env
set +o allexport

docker build -t $MAIN_TAG:latest .

docker build -t $STATIC_TAG:latest nginx/
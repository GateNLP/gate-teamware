#!/bin/bash

set -e

# set environment variables from file
set -o allexport
source .env
set +o allexport

docker build -t $IMAGE_REGISTRY$MAIN_IMAGE:$IMAGE_TAG .

docker build -t $IMAGE_REGISTRY$STATIC_IMAGE:$IMAGE_TAG --build-arg FILES_FROM=$IMAGE_REGISTRY$MAIN_IMAGE:$IMAGE_TAG nginx/

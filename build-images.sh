#!/bin/bash

set -e

# set environment variables from file
set -o allexport
source .env
set +o allexport

docker buildx build --load -t $IMAGE_REGISTRY$MAIN_IMAGE:$IMAGE_TAG --target backend .

docker buildx build --load -t $IMAGE_REGISTRY$STATIC_IMAGE:$IMAGE_TAG --target frontend .

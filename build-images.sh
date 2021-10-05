#!/bin/bash

set -e

docker build -t annotate-backend:latest .

docker build -t annotate-static:latest nginx/
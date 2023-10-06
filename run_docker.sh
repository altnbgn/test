#!/bin/bash

# install library
# apk add build-base linux-headers
docker run -it --rm --name ot-py-dev \
    -p 9192:50050 \
    -v $(pwd):/app \
    -w /app \
    python:3.9.12-slim sh 
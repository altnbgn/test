#!/bin/bash

# install library
# apk add build-base linux-headers
docker run -it --rm --name ot-py-dev-gpu \
    --gpus all \
    -p 9193:50050 \
    -v $(pwd):/app \
    -w /app \
    pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime sh 
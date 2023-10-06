#!/bin/bash -e

image_tag=0.1.4
image_name=ghcr.io/andorean/rockdetector
full_image_name=${image_name}:${image_tag}

DIR="$( cd "$( dirname "$0" )" && pwd )"
echo $DIR

# DOCKER_BUILDKIT=1 docker build -t "${full_image_name}" $DIR
# docker push "$full_image_name"

PLATFORM=linux/amd64

docker buildx inspect iot || docker buildx create --name=iot --driver=docker-container --platform linux/amd64,linux/arm64                    
docker buildx build --platform $PLATFORM \
    -t "$full_image_name" -f Dockerfile \
    . --push

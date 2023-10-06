#! /bin/bash

export SNYK_TOKEN=4f2ef7b8-1d80-40a5-990a-4e7535551080

docker run --rm -it \
    --env SNYK_TOKEN \
    -v /var/run/docker.sock:/var/run/docker.sock \
    snyk/snyk:docker snyk test --docker ghcr.io/andorean/ot-video-analyze/processor-worker:0.0.1
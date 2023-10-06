#!/bin/bash
SCRIPT_DIR=$(dirname "$0")
echo $SCRIPT_DIR

pushd $SCRIPT_DIR
PROCESSOR_POD_IP=172.20.10.12
TASKMANAGER_HOST=172.20.10.12
TASKMANAGER_PORT=9190

docker run -it --rm --name ot-processor-worker \
    -e PROCESSOR_POD_IP=$PROCESSOR_POD_IP \
    -e TASKMANAGER_HOST=$TASKMANAGER_HOST \
    -e TASKMANAGER_PORT=$TASKMANAGER_PORT \
    -p 50050:50050 \
    ghcr.io/andorean/ot-video-analyze/processor-worker:0.0.1

#!/bin/sh
POD_IP=${PROCESSOR_POD_IP:-'127.0.0.1'}
TASKMANAGER_HOST=${TASKMANAGER_HOST:-taskmanager.demo.svc.cluster.local}
TASKMANAGER_PORT=${TASKMANAGER_PORT:-'9999'}

echo "POD_IP: $POD_IP"
echo "TASKMANAGER_HOST: $TASKMANAGER_HOST"
echo "TASKMANAGER_PORT: $TASKMANAGER_PORT"

echo "update configs.ini"
sed -i "s/POD_IP/${POD_IP}/" /code/configs/configs.ini;
sed -i "s/TASKMANAGER_HOST/${TASKMANAGER_HOST}/" /code/configs/configs.ini;
sed -i "s/TASKMANAGER_PORT/${TASKMANAGER_PORT}/" /code/configs/configs.ini;

echo "check configs.ini"
cat /code/configs/configs.ini

echo "\nstart"

python /code/main.py
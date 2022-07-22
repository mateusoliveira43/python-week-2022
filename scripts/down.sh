#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
$ROOT/scripts/env.sh

for MODE in 'dev' 'prod'
do
    docker-compose \
    --file $ROOT/docker/docker-compose.$MODE.yaml \
    --project-directory $ROOT \
    down --volumes --rmi 'all'
done

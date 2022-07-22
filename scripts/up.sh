#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
$ROOT/scripts/env.sh

while read line; do
    if [[ "$line" == *'PROJECT_NAME='* ]]; then
        PROJECT_NAME=${line#*=}
    fi
done < $ROOT/.env

docker-compose \
--file $ROOT/docker/docker-compose.$1.yaml \
--project-directory $ROOT \
up

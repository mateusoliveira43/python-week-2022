#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
FILE="$ROOT/.env"
PROJECT_NAME='beerlog'

if ! test -f $FILE; then
    echo "PROJECT_NAME=$PROJECT_NAME" >> $FILE
    echo "WORK_DIR=/home/$PROJECT_NAME/$PROJECT_NAME" >> $FILE
    echo "USER_ID=$(id -u)" >> $FILE
    echo "GROUP_ID=$(id -g)" >> $FILE
    echo "HOST=0.0.0.0" >> $FILE
    echo "PORT=8000" >> $FILE
    echo ".env file created in project's root"
fi

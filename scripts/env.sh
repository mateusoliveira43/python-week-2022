#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
FILE="$ROOT/.env"
PROJECT_NAME='beerlog'
DATABASE_NAME="$PROJECT_NAME-database"

if ! test -f $FILE; then
    echo "BEERLOG_PROJECT_NAME=$PROJECT_NAME" >> $FILE
    echo "BEERLOG_WORK_DIR=/home/$PROJECT_NAME/$PROJECT_NAME" >> $FILE
    echo "BEERLOG_USER_ID=$(id -u)" >> $FILE
    echo "BEERLOG_GROUP_ID=$(id -g)" >> $FILE
    echo "BEERLOG_API_HOST=0.0.0.0" >> $FILE
    echo "BEERLOG_API_PORT=8000" >> $FILE
    echo "BEERLOG_DATABASE_SERVER=TRUE" >> $FILE
    echo "BEERLOG_DATABASE_NAME=$DATABASE_NAME" >> $FILE
    echo "BEERLOG_DATABASE_HOST=$DATABASE_NAME" >> $FILE
    echo "BEERLOG_DATABASE_PORT=5432" >> $FILE
    echo ".env file created in project's root"
fi

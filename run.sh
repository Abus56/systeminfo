#!/bin/bash

server=$1
user=$2
password=$3
docker build -t app_nginx .
docker run --rm -p 8081:8081 \
    -e SMTP_SERVER=$server \
    -e SMTP_USER=$user \
    -e SMTP_PASSWORD=$password \
    -v $PWD/files:/files -w /files --name=test app_nginx "/files/app.py"

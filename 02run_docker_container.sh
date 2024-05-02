#!/bin/bash

path=$(pwd)

sudo docker run \
--name list_am_parser \
-v ${path}/database.db:/home/list_parser/database.db \
-d \
--env-file ./.env \
--rm \
--log-driver syslog \
--log-opt tag=docker/{{.ImageName}} \
--log-opt syslog-address=unixgram:///dev/log \
list_parser make --file /home/list_parser/Makefile run
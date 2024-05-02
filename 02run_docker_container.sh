#!/bin/bash

path=$(pwd)

sudo docker run -v ${path}/database.db:/home/list_parser/database.db -it --env-file ./.env --rm list_parser make --file /home/list_parser/Makefile run
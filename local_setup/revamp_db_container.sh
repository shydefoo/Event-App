#!/usr/bin/env bash
docker stop app_db
docker container rm app_db
./docker_db_start.sh
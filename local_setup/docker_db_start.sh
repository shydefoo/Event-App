#!/usr/bin/env bash

docker run --name app_db \
-e ALLOW_EMPTY_PASSWORD=yes \
-e MYSQL_DATABASE=event_app_database \
-p 3306:3306 \
-d \
bitnami/mysql
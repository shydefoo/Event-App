#!/usr/bin/env bash

docker run --name app_db \
-e ALLOW_EMPTY_PASSWORD=yes \
-e MYSQL_DATABASE=event_app_database \
-p 3306:3306 \
-v local_db_vol:/bitnami/mysql/data \
-d bitnami/mysql
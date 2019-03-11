#!/usr/bin/env bash

container_ids=($(docker ps -aqf name=web_app))
if [[ "${container_ids[0]}" != "" ]]; then
    echo ${container_ids[0]}
    docker exec ${container_ids[0]} << EOF
        python src/manage.py shell < create_root_user.py
    EOF
    echo "Inserted new username into database"
else
    echo $(docker ps)
    echo "Could not find container"
fi
#!/usr/bin/env bash

echo "Setting up admin user.."
container_ids=($(docker ps -aqf name=web_app))
if [[ "${container_ids[0]}" != "" ]]; then
    echo ${container_ids[0]}
    docker exec ${container_ids[0]} /bin/bash -c 'python src/manage.py shell < src/app/utils/create_root_user.py'
else
    echo $(docker ps)
    echo "Could not find container"
fi
exit 1
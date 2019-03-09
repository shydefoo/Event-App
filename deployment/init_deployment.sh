#!/usr/bin/env bash

# Automation script to upload new image to server.
#Args:
# arg0 - user@server_ip_address
# arg1 - image tag
# arg2 - tar file name
# arg3 - path to save deployment folder
# arg4 - stack name
# 1) build docker image, take in arg1 for docker build -t option
# 2) save as tar file, docker save arg1 > arg2 (arg2 is the tar file)
# 3) upload deployment folder to server via scp, location dependent on arg3
# 4) cd into arg3
# 5) docker load -i arg2
# 6) docker stack deploy -c docker-compose.yml arg4
server_ip=ld-foosd@203.116.180.244
image_tag=entry-task:latest
tar_file_name=$3
save_path=$4
stack_name=$5

while [ "$1" != "" ]; do
    case $1 in
        -ip | --ip_address)     shift
                                server_ip=$1
                                ;;
        -t | --image_tag )      shift
                                image_tag=$1
                                ;;
        -f | --file_name )      shift
                                tar_file_name=$1
                                ;;
        -save | --save )        shift
                                save_path=$1
                                ;;
        -stack | --stack_name)  shift
                                stack_name=$1
    esac
    shift
done

echo "$server_ip"
echo "$image_tag"
echo "$tar_file_name"
echo "$save_path"
echo "$stack_name"

docker build -t $image_tag . && \
docker save $image_tag > $tar_file_name && \
scp $(pwd) $server_ip:$save_path && \
ssh $server_ip && cd $save_path && \
docker load -i $tar_file_name && \
docker stack deploy -c docker-compose.yml $stack_name

#!/usr/bin/env bash

# Automation script to upload new image to server. This script is to run from local machine
#Args:
# arg0 - user@server_ip_address
# arg1 - image tag
# arg2 - tar file name
# arg3 - path to save deployment folder
# arg4 - stack name
# 1) build docker image, take in arg1 for docker build -t option
# 2) save as tar file, docker save arg1 > arg2 (arg2 is the tar file)
# 3) upload whole deployment folder to server via scp, location dependent on arg3
# 4) cd into arg3
# 5) docker load -i arg2
# 6) docker stack deploy -c docker-compose.yml arg4
# Eg. ./init-deployment.sh -t entry-task:v1.9 -f entry-task-v1.9.tar -save /home/ld-sgdev/foosd/entry-task-v1.9 -stack et
server_ip=ld-foosd@203.116.180.244
image_tag=entry-task:latest
create_root=0
overwrite_stack=0 # rm stack currently used in server and deploy new stack with same name (to re-use docker volumes)

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
                                ;;
        --overwrite)            shift
                                overwrite_stack=$1
                                ;;
        --setup_admin)          shift
                                create_root=$1
                                ;;

    esac
    shift
done

echo "$server_ip"
echo "$image_tag"
echo "$tar_file_name"
echo "$save_path"
echo "$stack_name"

if [[ $overwrite_stack -eq 1 ]]; then
scp $server_ip << EOF
docker stack rm ${stack_name}
EOF

if [[ "$(docker images -q ${image_tag} 2> /dev/null)" == "" ]]; then
    echo "Building Docker Image...."
    docker build -t $image_tag ..
    echo "Docker Image built! Image tag: ${image_tag}"
else
    echo "Image ${image_tag} already exists"
fi

echo "Saving Docker image to tar file..."
docker save $image_tag > $tar_file_name
echo "Docker image saved to ${tar_file_name}"
echo "Copying deployment folder to ${save_path} at ${server_ip}"
scp -r $(pwd) $server_ip:$save_path



fi

ssh $server_ip << EOF
cd $save_path
export ENTRY_TASK_IMAGE=$image_tag

echo "untarring ${tar_file_name}"
docker load -i $tar_file_name

echo "deploying stack.."
docker stack deploy -c docker-compose.yml $stack_name
echo "waiting for stack to be deployed"
sleep 20s
docker stack ls
docker service ls
docker ps
EOF
echo "App Deployment complete."

if [[ $create_root -eq 1 ]]; then
    echo "Setting up admin account"
    ssh $server_ip << EOF
    cd $save_path
    ./admin-setup-script.sh
EOF
fi


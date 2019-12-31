#!/bin/bash

# This code is used to run AutoGrow4 that is inside of the docker
# from outside the docker. It also copies the results from within the
# docker container to the root_output_folder
temp_user_files=$1
outfolder=$2
echo "###################################"
echo $temp_user_files
echo $outfolder
echo "###################################"
# sudo docker run --rm  -v $temp_user_files \
#     --name autogrow
docker run -it autogrow4 \
    --name autogrow4 -/UserFiles/docker_json_vars.json


# CONTAINER_ID=$(sudo docker ps -alq)
CONTAINER_ID=$(docker ps -alq)
echo "###################################"
echo "In THIS CONTAINER_ID: "$CONTAINER_ID
echo "###################################"
docker cp $CONTAINER_ID:/Outputfolder.zip $outfolder
chmod -R a+rwx $outfolder

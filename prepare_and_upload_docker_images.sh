#!/bin/bash


echo -n "Do you want to remove the existing images (y/n)? "
read remove_existing_images

read -p 'Enter Docker Hub username: ' username
read -sp 'Enter Docker Hub Password: ' password
echo -e "\n"


read -p 'Enter image version: ' tag
tag=${tag:-latest}

export DOCKER_VERSION=18.09.0
export DOCKER_CHANNEL=stable

echo "--------------------------"
echo $tag

echo "Logging in to docker hub..."
docker login -u $username -p $password

images=(docker_events_notifier neo4j_service openstack_querier)

if [ "$remove_existing_images" != "${remove_existing_images#[Yy]}" ] ;then
    echo "Removing existing images..."
    for i in "${images[@]}"; do 
	echo "============================================="
	echo "Stopping and removing $i" 
        docker rm $(docker stop $(docker ps -a --filter ancestor="$i" --format="{{.ID}}" -q)) 
	docker rmi --force "$i";
	docker rmi --force $username/$i;
	docker images | grep $i | tr -s ' ' | cut -d ' ' -f 2 | xargs -I {} docker rmi $username/$i:{}  
        echo "Stopped and removed $i"
    done
fi

echo "Copying files in folders..."

rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git docker_events_notifier docker/docker_events_notifier/cloud_reconnoiterer/

rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git graph_service_resource docker/neo4j_service/cloud_reconnoiterer/
rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git graph_service_api docker/neo4j_service/cloud_reconnoiterer/


rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git neo4jservice_os_mediator docker/openstack_querier/cloud_reconnoiterer/
rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git notifications_subscriber docker/openstack_querier/cloud_reconnoiterer/
rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git openstack_querier docker/openstack_querier/cloud_reconnoiterer/

cp configs/openstack_info.json docker/openstack_querier/cloud_reconnoiterer/
cp configs/event_component_mapping.json docker/openstack_querier/cloud_reconnoiterer/


docker build --build-arg DOCKER_VERSION=$DOCKER_VERSION --build-arg DOCKER_CHANNEL=$DOCKER_CHANNEL  -t docker_events_notifier docker/docker_events_notifier --no-cache
docker tag docker_events_notifier $username/docker_events_notifier:$tag
docker push $username/docker_events_notifier:$tag

docker build -t neo4j_service docker/neo4j_service --no-cache
docker tag neo4j_service $username/neo4j_service:$tag
docker push $username/neo4j_service:$tag

docker build -t openstack_querier docker/openstack_querier --no-cache
docker tag openstack_querier $username/openstack_querier:$tag
docker push $username/openstack_querier:$tag

echo "Logging out from docker hub..."
docker logout

echo "Exiting successfully..."
exit 0

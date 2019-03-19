#!/bin/bash


echo -n "Do you want to remove the existing images (y/n)? "
read remove_existing_images

read -p 'Enter Docker Hub username: ' username
read -sp 'Enter Docker Hub Password: ' password
echo -e "\n"


read -p 'Enter image version: ' tag
tag=${tag:-latest}

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
        echo "Stopped and removed $i"
    done
fi

echo "Copying files in folders..."

rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git docker_events_notifier docker/docker_events_notifier/docker_events_notifier

rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git graph_service_resource docker/neo4j_service/graph_service_resource
rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git graph_service_api docker/neo4j_service/graph_service_api


rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git neo4jservice_os_mediator docker/openstack_querier/neo4jservice_os_mediator
rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git notifications_subscriber docker/openstack_querier/notifications_subscriber
rsync -rv --exclude=venv --exclude=__pycache__ --exclude=.idea --exclude=.git openstack_querier docker/openstack_querier/openstack_querier

cp configs/openstack_info.json docker/openstack_querier/
cp configs/event_component_mapping.json docker/openstack_querier/

echo "Building, tagging, and uploading Docker images..."
for i in "${images[@]}"; do
	echo "============================================="
	echo "Building, tagging and uploading $i"
	docker build -t "$i" docker/"$i"/ --no-cache
        docker tag "$i" $username/$i:$tag
        docker push $username/$i:$tag
        echo "Built, tagged, and uploaded $i"
    done

echo "Logging out from docker hub..."
docker logout

echo "Exiting successfully..."
exit 0

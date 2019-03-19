#!/bin/sh


echo -n "Do you want to remove the existing images (y/n)? "
read remove_existing_images

read -p 'Enter Docker Hub username: ' username
read -sp 'Enter Docker Hub Password: ' password
echo -e "\n"


read -p 'Enter image version: ' tag
tag=${tag:-latest}

echo "Logging in to docker hub..."
docker login -u $username -p $password

images=(docker_events_notifier neo4j_service openstack_querier)

if [ "$remove_existing_images" != "${remove_existing_images#[Yy]}" ] ;then
    echo "Removing existing images..."
    for i in "${images[@]}"; do 
	docker stop "$i"
        docker rm $(docker stop $(docker ps -a --filter ancestor="$i" --format="{{.ID}}" -q)) 
	docker rmi --force "$i";
        echo "Stopped and removed $i"
    done
fi

echo "Copying files in folders..."

cp -r docker_events_notifier docker/docker_events_notifier/docker_events_notifier

cp -r graph_service_resource docker/neo4j_service/graph_service_resource
cp -r graph_service_api docker/neo4j_service/graph_service_api


cp -r neo4jservice_os_mediator docker/openstack_querier/neo4jservice_os_mediator
cp -r notifications_subscriber docker/openstack_querier/notifications_subscriber
cp -r openstack_querier docker/openstack_querier/openstack_querier

cp configs/openstack_info.json docker/openstack_querier/
cp configs/event_component_mapping.json docker/openstack_querier/

echo "Building, tagging, and uploading Docker images..."
for i in "${images[@]}"; do 
	docker build -t "$i" docker/"$i"/ --no-cache
        docker tag "$i" $username/$i:$tag
        docker push $username/$i
        echo "Built, tagged, and uploaded $i"
    done

echo "Logging out from docker hub..."
docker logout

echo "Exiting successfully..."
exit 0

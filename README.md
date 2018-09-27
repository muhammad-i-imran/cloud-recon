# Python-based Service to Store Openstack Cloud Infrastructure Data in a Neo4j Database

The code is to be used in two docker images--`openstack-neo4j-service` and `openstack-querier`.  `openstack-neo4j-service` image should contain `graph_service_api` and `graph_service_resource` modules. `openstack-querier` image should contain `neo4jservice_os_mediator`, `openstack_querier`, and `graph_service_interface_schema` modules.

## Steps:
- Copy `graph_service_api` and `graph_service_resource` modules in `neo4j_service_docker` folder and run the following command after entering the directory: 
`sudo  docker build -t <image-name> .`
- Copy `neo4jservice_os_mediator`, `openstack_querier`, and `graph_service_interface_schema` modules in `openstack_querier_docker` and run the following command after entering the directory: 
`sudo  docker build -t <image-name> .`
- Upload the images to a docker registry.
- Update `.env` file and provide information.
- Provide Envrionment variables required in `docker-compose.yml` file
- Run `docker-compose.yml` file by running the following command: 
`sudo docker-compose up -d`

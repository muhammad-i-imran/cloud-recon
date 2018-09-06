FROM ubuntu:latest
RUN apt-get update -y

mkdir /openstack-neo4j-service
WORKDIR /openstack-neo4j-service

RUN apt-get install -y python-pip python-dev build-essential

COPY ../graph-service-interface-schema  /openstack-neo4j-service/
COPY ../neo4jservice-os-mediator  /openstack-neo4j-service/
COPY ../openstack-querier  /openstack-neo4j-service/

RUN pip install -r requirements.txt

CMD ["/bin/bash"]

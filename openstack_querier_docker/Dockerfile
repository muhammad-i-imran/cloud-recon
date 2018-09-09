FROM ubuntu:latest
RUN apt-get update -y

RUN mkdir -p  /openstack-neo4j-service
WORKDIR /openstack-neo4j-service

RUN apt-get install -y python-pip python-dev build-essential nano

COPY graph-service-interface-schema  /openstack-neo4j-service/graph-service-interface-schema
COPY neo4jservice-os-mediator  /openstack-neo4j-service/neo4jservice-os-mediator
COPY openstack-querier  /openstack-neo4j-service/openstack-querier
COPY requirements.txt /
RUN pip install -r /requirements.txt

CMD ["/bin/bash"]

FROM ubuntu:latest
RUN apt-get update -y

RUN mkdir -p  /openstack_neo4j_service
WORKDIR /openstack_neo4j_service

RUN apt-get install -y python-pip python-dev build-essential nano

COPY graph_service_interface_schema  /openstack_neo4j_service/graph_service_interface_schema
COPY neo4jservice_os_mediator  /openstack_neo4j_service/neo4jservice_os_mediator
COPY openstack_querier  /openstack_neo4j_service/openstack_querier
COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN cd /openstack_neo4j_service/graph_service_interface_schema / && python setup.py sdist
RUN pip install graphserviceschema==0.1 --no-index --find-links file:///openstack_neo4j_service/graph_service_interface_schema/dist/

RUN cd /openstack_neo4j_service/openstack_querier / && python setup.py sdist
RUN pip install openstackqueryapi==0.1 --no-index --find-links file:///openstack_neo4j_service/openstack_querier/dist/

WORKDIR /openstack_neo4j_service
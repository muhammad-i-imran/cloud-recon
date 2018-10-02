FROM ubuntu:latest
RUN apt-get update -y

RUN mkdir -p /openstack_neo4j_service

RUN apt-get install -y python-pip python-dev build-essential nano netcat

COPY graph_service_api  /openstack_neo4j_service/graph_service_api
COPY graph_service_resource  /openstack_neo4j_service/graph_service_resource
COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN cd /openstack_neo4j_service/graph_service_api/ && python setup.py sdist
RUN pip install neo4japi==0.1 --no-index --find-links file:///openstack_neo4j_service/graph_service_api/dist/

WORKDIR /openstack_neo4j_service


ENTRYPOINT ["python"]
CMD ["/openstack_neo4j_service/graph_service_resource/main.py"]


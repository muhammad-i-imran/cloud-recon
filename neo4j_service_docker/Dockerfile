FROM ubuntu:latest
RUN apt-get update -y

RUN mkdir -p /openstack_neo4j_service


RUN apt-get install -y software-properties-common python-pip python-dev build-essential nano netcat

RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y
RUN apt-get install -y python3.6 python3.6-dev python3-pip 
RUN python3.6 -m pip install pip --upgrade


COPY graph_service_api  /openstack_neo4j_service/graph_service_api
COPY graph_service_resource  /openstack_neo4j_service/graph_service_resource
COPY requirements.txt /
RUN python3.6 -m pip install -r /requirements.txt

RUN cd /openstack_neo4j_service/graph_service_api/ && python setup.py sdist
RUN python3.6 -m pip install neo4japi==0.1 --no-index --find-links file:///openstack_neo4j_service/graph_service_api/dist/

WORKDIR /openstack_neo4j_service


ENTRYPOINT ["python3.6"]
CMD ["/openstack_neo4j_service/graph_service_resource/main.py"]


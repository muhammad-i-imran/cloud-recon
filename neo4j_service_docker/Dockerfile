FROM ubuntu:latest
RUN apt-get update -y

RUN mkdir -p /openstack-neo4j-service
WORKDIR /openstack-neo4j-service

RUN apt-get install -y python-pip python-dev build-essential nano 

COPY graph-service-api  /openstack-neo4j-service/graph-service-api
COPY graph-service-resource  /openstack-neo4j-service/graph-service-resource
COPY requirements.txt /
RUN pip install -r /requirements.txt
# ENTRYPOINT ["python"]
# CMD ["/openstack-neo4j-service/graph-service-resource/main.py"]
CMD ["/bin/bash"]
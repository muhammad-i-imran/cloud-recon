FROM ubuntu:latest
RUN apt-get update -y

mkdir /openstack-neo4j-service
WORKDIR /openstack-neo4j-service

RUN apt-get install -y python-pip python-dev build-essential
COPY .  /openstack-neo4j-service/

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/openstack-neo4j-service/graph-service-resource/main.py"]

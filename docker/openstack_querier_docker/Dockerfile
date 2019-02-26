FROM python:3


#RUN mkdir -p  /openstack_neo4j_service
WORKDIR /openstack_neo4j_service

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common python-pip python-dev build-essential nano netcat


COPY openstack_neo4j_service  /
COPY requirements.txt /
COPY openstack_info.json /

RUN python3 -m pip install -r /requirements.txt

# RUN cd /openstack_neo4j_service/graph_service_interface_schema / && python setup.py sdist
# RUN pip install graphserviceschema==0.1 --no-index --find-links file:///openstack_neo4j_service/graph_service_interface_schema/dist/

# RUN cd /openstack_neo4j_service/openstack_querier / && python setup.py sdist
# RUN python3 -m pip install openstackqueryapi==0.1 --no-index --find-links file:///openstack_neo4j_service/openstack_querier/dist/

COPY wait-for-neo4j-service.sh /
RUN chmod +x /wait-for-neo4j-service.sh

WORKDIR /openstack_neo4j_service/neo4jservice_os_mediator

ENTRYPOINT ["/bin/bash", "-c", "/wait-for-neo4j-service.sh"]
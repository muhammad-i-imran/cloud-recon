FROM python:3

RUN mkdir -p  /cloud-reconnoiterer
WORKDIR /cloud-reconnoiterer

COPY graph_service_api  ./
COPY graph_service_resource ./
COPY requirements.txt ./
COPY wait-for-neo4j.sh ./

RUN python3 -m pip install -r ./requirements.txt

# RUN cd /openstack_neo4j_service/graph_service_api/ && python setup.py sdist
# RUN python3 -m pip install neo4japi==0.1 --no-index --find-links file:///openstack_neo4j_service/graph_service_api/dist/

# RUN chmod +x ./wait-for-neo4j.sh  #should already have +x mode

ENTRYPOINT ["/bin/bash", "-c", "./wait-for-neo4j.sh"]
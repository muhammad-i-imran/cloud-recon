FROM python:3

ARG NEO4J_SERVICE_HOST=127.0.0.1
ARG NEO4J_SERVICE_PORT=15135

ENV NEO4J_SERVICE_HOST "127.0.0.1"
ENV NEO4J_SERVICE_PORT "15135"


RUN mkdir -p  /cloud-reconnoiterer
WORKDIR /cloud-reconnoiterer

COPY neo4jservice_os_mediator  ./
COPY openstack_querier ./
COPY notifications_subscriber ./
COPY requirements.txt ./
COPY openstack_info.json ./
COPY event_component_mapping.json ./
COPY wait-for-neo4j-service.sh /

RUN python3 -m pip install -r ./requirements.txt

RUN chmod +x /wait-for-neo4j-service.sh
ENTRYPOINT ["./wait-for-neo4j-service.sh", "$NEO4J_SERVICE_HOST", "$NEO4J_SERVICE_PORT", "python", "./neo4jservice_os_mediator/main.py"]

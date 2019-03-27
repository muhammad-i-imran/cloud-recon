FROM python:3

ARG NEO4J_SERVICE_HOST=127.0.0.1
ARG NEO4J_SERVICE_PORT=15135

ENV NEO4J_SERVICE_HOST "127.0.0.1"
ENV NEO4J_SERVICE_PORT "15135"

RUN apt-get update -y && apt-get install -y netcat

COPY cloud_reconnoiterer/ /cloud_reconnoiterer
WORKDIR /cloud_reconnoiterer

#RUN python3 -m pip install -r ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


ENV PYTHONPATH=./neo4jservice_os_mediator:./openstack_querier:./notifications_subscriber:$PYTHONPATH

RUN chmod +x ./wait-for-neo4j-service.sh
ENTRYPOINT ["./wait-for-neo4j-service.sh", "$NEO4J_SERVICE_HOST", "$NEO4J_SERVICE_PORT", "python3", "./neo4jservice_os_mediator/main.py"]

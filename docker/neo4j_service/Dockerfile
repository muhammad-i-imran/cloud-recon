FROM python:3

ARG NEO4J_DATABASE_HOST=127.0.0.1
ARG NEO4J_DATABASE_PORT=15135

ENV NEO4J_DATABASE_HOST=$NEO4J_DATABASE_HOST
ENV NEO4J_DATABASE_PORT=$NEO4J_DATABASE_PORT

RUN mkdir -p  /cloud-reconnoiterer
WORKDIR /cloud-reconnoiterer

COPY graph_service_api  ./
COPY graph_service_resource ./
COPY requirements.txt ./
COPY wait-for-neo4j.sh ./

RUN python3 -m pip install -r ./requirements.txt

RUN chmod +x ./wait-for-neo4j.sh
ENTRYPOINT ["./wait-for-neo4j.sh", "${NEO4J_DATABASE_HOST}", "${NEO4J_DATABASE_PORT}", "python", "./graph_service_resource/main.py"]
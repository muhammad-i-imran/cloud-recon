FROM python:3

#ARG NEO4J_DATABASE_HOST=127.0.0.1
#ARG NEO4J_DATABASE_PORT=15135

ENV NEO4J_DATABASE_HOST "127.0.0.1"
ENV NEO4J_DATABASE_PORT "7474"

COPY cloud_reconnoiterer/ /cloud_reconnoiterer
WORKDIR /cloud_reconnoiterer

# RUN python3 -m pip install -r ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


ENV PYTHONPATH="./graph_service_api:./graph_service_resource:$PYTHONPATH"

RUN chmod +x ./wait-for-neo4j.sh
ENTRYPOINT ["./wait-for-neo4j.sh", "$NEO4J_DATABASE_HOST", "$NEO4J_DATABASE_PORT", "python3", "./graph_service_resource/main.py"]

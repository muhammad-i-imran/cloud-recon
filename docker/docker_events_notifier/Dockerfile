FROM python:3


ARG RABBITMQ_URL_DOCKER=amqp://user:password@localhost:5672
ARG RABBITMQ_HOST=localhost
ARG RABBITMQ_PORT=5672
ARG DOCKER_VERSION=18.09.0
ARG RABBITMQ_PORT=5672
ARG DOCKER_CHANNEL=stable

ENV RABBITMQ_URL_DOCKER=$RABBITMQ_URL_DOCKER
ENV RABBITMQ_HOST=$RABBITMQ_HOST
ENV RABBITMQ_PORT=$RABBITMQ_PORT
ENV DOCKER_CHANNEL=$DOCKER_CHANNEL
ENV DOCKER_VERSION=$DOCKER_VERSION


RUN apt-get update -y && apt-get install -y netcat

COPY cloud_reconnoiterer/ /cloud_reconnoiterer
WORKDIR /cloud_reconnoiterer

#RUN python3 -m pip install -r ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


# Install docker client
RUN curl -fsSL "https://download.docker.com/linux/static/${DOCKER_CHANNEL}/x86_64/docker-${DOCKER_VERSION}.tgz" | tar -xzvC /usr/local/bin --strip=1 docker/docker

RUN echo "if [ -e /var/run/docker.sock ]; then chown root:root /var/run/docker.sock; fi" >> /home/.bashrc

# VOLUME /var/run/docker.sock /var/run/docker.sock


RUN chmod +x ./wait-for-rabbitmq.sh

ENTRYPOINT ./wait-for-rabbitmq.sh "$RABBITMQ_HOST" "$RABBITMQ_PORT" "python3" "./docker_events_notifier/docker_events_listener.py"

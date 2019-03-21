FROM python:3

ARG RABBITMQ_URL_DOCKER
ARG DOCKER_VERSION=18.09.0
ARG DOCKER_CHANNEL=stable

ENV RABBITMQ_URL_DOCKER=$RABBITMQ_URL_DOCKER
ENV DOCKER_CHANNEL=$DOCKER_CHANNEL
ENV DOCKER_VERSION=$DOCKER_VERSION

COPY cloud_reconnoiterer/ /cloud_reconnoiterer
WORKDIR /cloud_reconnoiterer

#RUN python3 -m pip install -r ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


# Install docker client    
RUN curl -fsSL "https://download.docker.com/linux/static/${DOCKER_CHANNEL}/x86_64/docker-${DOCKER_VERSION}.tgz" | tar -xzvC /usr/local/bin --strip=1 docker/docker

RUN echo "if [ -e /var/run/docker.sock ]; then chown root:root /var/run/docker.sock; fi" >> /home/.bashrc

VOLUME /var/run/docker.sock

ENTRYPOINT ["python3","./docker_events_notifier/docker_events_listener.py"]

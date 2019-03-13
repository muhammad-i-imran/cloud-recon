FROM python:3

ARG RABBITMQ_URL_DOCKER

ENV RABBITMQ_URL_DOCKER=$RABBITMQ_URL_DOCKER
ENV DOCKER_CHANNEL stable
ENV DOCKER_VERSION 18.03.1-ce


RUN mkdir -p  /cloud-reconnoiterer
WORKDIR /cloud-reconnoiterer

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD docker_events_notifier ./docker_events_notifier

# Install docker client    
RUN curl -fsSL "https://download.docker.com/linux/static/${DOCKER_CHANNEL}/x86_64/docker-${DOCKER_VERSION}.tgz" | tar -xzvC /usr/local/bin --strip=1 docker/docker

RUN echo "if [ -e /var/run/docker.sock ]; then chown root:root /var/run/docker.sock; fi" >> /home/.bashrc
VOLUME /var/run/docker.sock

ENTRYPOINT ["python","./docker_events_notifier/docker_events_listener.py"]
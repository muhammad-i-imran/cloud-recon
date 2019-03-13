FROM python:3

ARG RABBITMQ_URL_DOCKER

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD docker_events_notifier ./docker_events_notifier

# Install docker client    
ENV DOCKER_CHANNEL stable
ENV DOCKER_VERSION 18.03.1-ce
RUN curl -fsSL "https://download.docker.com/linux/static/${DOCKER_CHANNEL}/x86_64/docker-${DOCKER_VERSION}.tgz" | tar -xzvC /usr/local/bin --strip=1 docker/docker

RUN echo "if [ -e /var/run/docker.sock ]; then chown root:root /var/run/docker.sock; fi" >> /home/.bashrc
VOLUME /var/run/docker.sock

ENTRYPOINT ["python","./docker_events_notifier/docker_events_listener.py"]
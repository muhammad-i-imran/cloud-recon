from docker.client import Client
from threading import Thread
from publisher import DockerNotificationPublisher
import sys
import os
import json
import socket

import logging


LOG = logging.getLogger(__name__)

class DockerEventListener(object):
    def __init__(self, unix_socket_url):
        self.client = Client(base_url=unix_socket_url, timeout=300)

    def listen(self, filters, forwarding_type):
        publisher = DockerNotificationPublisher.init_with_url_parameter(url=rabbit_mq_url)

        events = self.client.events(filters= filters, decode=True)
        notification_format = {"priority": "INFO", "payload": None, "event_type": None, "publisher_id": socket.gethostname()}  # later use; https://docs.openstack.org/nova/pike/reference/notifications.html
        for event in events:
            notification_format["payload"] = event
            notification_format["event_type"] = forwarding_type
            LOG.debug("Calling publish_events() from docker_events_listener")
            try:
                publisher.publish_events(event_type=forwarding_type, payload=json.dumps(notification_format))
            except Exception as ex:
                print("Exception occured while publishing events: %s" % str(ex))
                publisher.close()

def main():
    unix_socket_url = "unix://var/run/docker.sock"
    event_listeners = DockerEventListener(unix_socket_url=unix_socket_url)

    event_types = {
        "start": "docker.container.create.end",
        "stop": "docker.container.stop.end"
    }
    filters = {
        "type": "container",
        "event": None
    }
    for event_type in event_types:
        filters["event"] = event_type
        thread = Thread(target=event_listeners.listen, args=(filters, event_types[event_type]))
        try:
            LOG.info("Starting threads.")
            thread.start() #run forever until interrupted
        except (SystemExit, KeyboardInterrupt):
            LOG.exception("Exception occured.")
            sys.exit()

if __name__ == '__main__':
    rabbit_mq_url = os.getenv("RABBITMQ_URL_DOCKER", "amqp://user:bitnami@localhost:30002/")
    main()
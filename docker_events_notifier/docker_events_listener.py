from docker.client import Client
from threading import Thread
from publisher import DockerNotificationPublisher
import sys
import os
import json

class DockerEventListener(object):
    def __init__(self, unix_socket_url, publisher_instance):
        self.client = Client(base_url=unix_socket_url)
        self.publisher = publisher_instance
        # self.notification_format = {"priority": "INFO", "payload": None, "event_type": None, "publisher_id": "docker"}

    def listen(self, filters, forwarding_type):
        events = self.client.events(filters= filters, decode=True)
        notification_format = {"priority": "INFO", "payload": None, "event_type": None, "publisher_id": "docker"}  # later use; https://docs.openstack.org/nova/pike/reference/notifications.html
        for event in events:
            notification_format["payload"] = event
            notification_format["event_type"] = forwarding_type
            self.publisher.publish_events(event_type=forwarding_type, payload=json.dumps(notification_format))

def main():
    publisher = DockerNotificationPublisher.init_with_url_parameter(url=rabbit_mq_url)
    unix_socket_url = "unix://var/run/docker.sock"
    event_listeners = DockerEventListener(unix_socket_url=unix_socket_url, publisher_instance=publisher)
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
            thread.start() #run forever until interrupted
        except (SystemExit, KeyboardInterrupt):
            sys.exit()

if __name__ == '__main__':
    rabbit_mq_url = os.getenv("RABBITMQ_URL_DOCKER", "amqp://user:bitnami@localhost:30002/")
    main()
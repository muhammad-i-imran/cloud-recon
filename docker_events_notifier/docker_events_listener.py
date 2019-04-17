from docker.client import Client
from threading import Thread
from publisher import DockerNotificationPublisher
import sys
import os
import json
import socket
import requests
from logging_config import Logger

LOGS_FILE_PATH = os.getenv('LOGS_FILE_PATH', '/cloud_reconnoiterer/logs/cloud_reconnoiterer.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

logger = Logger(log_file_path=LOGS_FILE_PATH, log_level=LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

class DockerEventListener(object):
    def __init__(self, unix_socket_url):
        self.client = Client(base_url=unix_socket_url, timeout=300)

        try:
            running_containers = self.client.containers()
            response = requests.get('http://169.254.169.254/openstack/2012-08-10/meta_data.json')
            for container in running_containers:
                response_json = response.json()
                container["id"] = container["Id"]
                container["name"] = container["Names"][0]
                del container["Id"]
                del container["Names"]

                container["server_id"] = response_json["uuid"]
                container["server_name"] = response_json["name"]
                self._publish_events(running_containers, "docker.container.list")
        except Exception as ex:
            logger.error("Exception occured: {0}".format(str(ex)))

    def listen(self, filters, forwarding_type):
        events = self.client.events(filters= filters, decode=True)
        self._publish_events(events, forwarding_type)

    def _publish_events(self, events_data, forwarding_type):
        publisher = DockerNotificationPublisher.init_with_url_parameter(url=rabbit_mq_url)
        notification_format = {"priority": "INFO", "payload": None, "event_type": None,
                               "publisher_id": socket.gethostname()}  # later use; https://docs.openstack.org/nova/pike/reference/notifications.html
        for event in events_data:
            notification_format["payload"] = event
            notification_format["event_type"] = forwarding_type
            logger.debug("Calling publish_events() from docker_events_listener")
            try:
                publisher.publish_events(event_type=forwarding_type, payload=json.dumps(notification_format))
            except Exception as ex:
                logger.error("Exception occured while publishing events: {0}".format(str(ex)))
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
            logger.info("Starting threads.")
            thread.start() #run forever until interrupted
        except (SystemExit, KeyboardInterrupt):
            logger.exception("Exception occured.")
            sys.exit()

if __name__ == '__main__':
    rabbit_mq_url = os.getenv("RABBITMQ_URL_DOCKER", "amqp://user:bitnami@localhost:30002/")
    main()
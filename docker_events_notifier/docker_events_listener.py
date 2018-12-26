from docker.client import Client
from threading import Thread
from publisher import DockerNotificationPublisher
import sys

class DockerEventListener(object):
    def __init__(self):
        self.client = Client(base_url='unix://var/run/docker.sock')
        self.publisher = DockerNotificationPublisher.init_with_url_parameter(url='amqp://user:bitnami@localhost:32770')

    def listen(self, filters, forwarding_type):
        print(str(filters))
        events = self.client.events(filters= filters, decode=True)
        for event in events:

            self.publisher.publish_events(event_type=forwarding_type, payload=str(event))
            print("event: " + str(event) + ", forward_to: " + forwarding_type)


def main():
    event_listeners = DockerEventListener()
    event_types = {"start": "docker.container.create.end", "destroy": "docker.container.delete.end"}
    threads = []
    for event_type in event_types:
        filters = {
            "type" : "container",
            "event" : event_type
        }
        thread = Thread(target=event_listeners.listen, args=(filters, event_types[event_type]))
        try:
            threads.append(thread)
            thread.start() #run forever until interrupted
        except (SystemExit, KeyboardInterrupt):
            # if thread.is_alive():
            print("interrupted")
            sys.exit()

if __name__ == '__main__':
    main()

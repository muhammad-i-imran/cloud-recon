import os

import pika


class DockerNotificationSubscriber(object):
    def __init__(self, parameter):
        self.connection = pika.BlockingConnection(parameter)
        self.channel = self.connection.channel()
        self.exchange_name = 'docker'
        self.topic_name = 'docker_notifications'
        self.events = ["docker.container.create.end",
                       "docker.container.stop.end"]  # events naming conventions are kept same as openstack's notification namings

        self.create_exchange()
        self.declare_queue()
        self.bind_queues()

    @classmethod
    def init_with_connection_paramters(cls, host, port, username, password, **connection_options):
        credentials = pika.PlainCredentials(username=username, password=password)
        connection_parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials,
                                                          **connection_options)
        return cls(connection_parameters)

    @classmethod
    def init_with_url_parameter(cls, url):
        url_parameter = pika.URLParameters(url)
        return cls(url_parameter)

    def event_callback(self, channel, method, properties, payload):
        if not method.routing_key.startswith("docker."):
            return

        print("Event: " + method.routing_key)
        print("Payload: " + str(payload))

        # payload...
        ##handle event here...

    def create_exchange(self):
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type='topic')

    def declare_queue(self):
        declared_queue = self.channel.queue_declare(exclusive=True)
        self.queue_name = declared_queue.method.queue

    def bind_queues(self):
        for event in self.events:
            self.channel.queue_bind(exchange=self.exchange_name,
                                    queue=self.queue_name,
                                    routing_key=event)

    def consume_events(self):
        self.channel.basic_consume(self.event_callback, queue=self.queue_name, no_ack=True)
        self.channel.start_consuming()

    def close_channel(self):
        if self.channel:
            self.channel.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()


### for testing purpose only
def main():
    subscriber = DockerNotificationSubscriber.init_with_url_parameter(url=rabbit_mq_url)
    subscriber.consume_events()


if __name__ == '__main__':
    rabbit_mq_url = os.getenv("RABBITMQ_URL_DOCKER", 'amqp://user:bitnami@localhost:30002')
    main()

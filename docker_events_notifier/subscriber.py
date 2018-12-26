import pika

class DockerNotificationSubscriber(object):
    def __init__(self, parameter):
        self.connection = pika.BlockingConnection(parameter)
        self.channel = self.connection.channel()
        self.events = ["container.create.end", "container.delete.end"] # events naming conventions are kept same as openstack's notification namings

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
        print("In call back")
        if not method.exchange.startswith("docker."):
            return
        event_name = method.exchange[len("docker."):]
        print(event_name)
        is_event_valid = True if event_name in self.events else False
        if not is_event_valid:
            return

        print("Event: " + event_name)
        print("Payload: " + str(payload))

        # payload...
        ##handle event here...

    def consume_events(self):
        for event in self.events:
            exchange_name = "docker.{0}".format(event)
            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type="fanout"
            ) # exchange type 'fanout' is better for event notifcations. since it broadcasts messages to all queues
            result = self.channel.queue_declare(exclusive=True)
            queue = result.method.queue

            self.channel.queue_bind(exchange=exchange_name, queue=queue)
            self.channel.basic_consume(self.event_callback, queue=queue, no_ack=True)

        self.channel.start_consuming()

    def close_channel(self):
        self.channel.close()

    def close_connection(self):
        self.connection.close()

### for testing purpose only
def main():
    subscriber = DockerNotificationSubscriber.init_with_url_parameter(url='amqp://user:bitnami@localhost:32770')
    subscriber.consume_events()
if __name__ == '__main__':
    main()
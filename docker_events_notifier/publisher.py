import pika

class DockerNotificationPublisher(object):
    def __init__(self, parameter):
        self.connection = pika.BlockingConnection(parameter)
        self.channel = self.connection.channel()
        # self.prefix = 'docker.'
        self.allowed_event_types = ["docker.container.create.end", "docker.container.delete.end"]

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

    def publish_events(self, event_type, payload):
        if not event_type in self.allowed_event_types:  # only allow listed event types
            return
        exchange_name =  event_type
        routing_key = ''
        print("exchange_name: " + exchange_name)
        self.channel.basic_publish(exchange=exchange_name,
                                   routing_key=routing_key,
                                   body=payload)

    def close_channel(self):
        self.channel.close()

    def close_connection(self):
        self.connection.close()
import pika


class DockerNotificationPublisher(object):
    def __init__(self, parameter):
        self.connection = pika.BlockingConnection(parameter)
        self.channel = self.connection.channel()
        self.exchange_name = 'docker'
        self.topic = 'docker_notifications'
        self.routing_key = 'docker_notifications.info'
        self.allowed_event_types = ["docker.container.create.end", "docker.container.stop.end"]

        self.create_exchange()

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

    def create_exchange(self):
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type='topic')

    def publish_events(self, event_type, payload):
        if not event_type in self.allowed_event_types:  # only allow listed event types
            return
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=self.routing_key,
                                   body=payload,
                                   properties=pika.BasicProperties(
                                       content_type="application/json",
                                       content_encoding="ascii-8bit",
                                       delivery_mode=2 # for persistence, in case the subscriber crashes, the messages will still be in the queue
                                       # headers=self.headers,
                                       # delivery_mode=self.delivery_mode,
                                       # priority=self.priority,
                                       # correlation_id=self.correlation_id,
                                       # reply_to=self.reply_to,
                                       #
                                       # message_id=self.message_id,
                                       # timestamp=self.timestamp,
                                       # type=self.type,
                                       # user_id=self.user_id,
                                       # app_id=self.app_id
                                   ))

    def close_channel(self):
        if self.channel:
            self.channel.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()

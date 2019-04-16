import pika
import uuid
import time
import os

from logging_config import Logger

LOGS_FILE_PATH = os.getenv('LOGS_FILE_PATH', '/cloud-reconnoiterer/logs/cloud-reconnoiterer.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

logger = Logger(log_file_path=LOGS_FILE_PATH, log_level=LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

class DockerNotificationPublisher(object):
    def __init__(self, parameter):
        logger.info("Creating blocking connection.")
        self.connection = pika.BlockingConnection(parameter)
        logger.info("Creating channel.")
        self.channel = self.connection.channel()
        self.exchange_name = 'docker'
        self.topic = 'docker_notifications'
        self.routing_key = 'docker_notifications.info'
        self.allowed_event_types = ["docker.container.create.end", "docker.container.stop.end", "docker.container.list"]

        self.create_exchange()

    @classmethod
    def init_with_connection_paramters(cls, host, port, username, password, **connection_options):
        logger.debug("Declaring plain credential.")
        credentials = pika.PlainCredentials(username=username, password=password)
        logger.debug("Creating connection parameters")
        connection_parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials,
                                                          **connection_options)
        return cls(connection_parameters)

    @classmethod
    def init_with_url_parameter(cls, url):
        url_parameter = pika.URLParameters(url)
        return cls(url_parameter)

    def create_exchange(self):
        logger.info("Declared RabbitMQ exchange.".format(self.exchange_name))
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type='topic')

    def publish_events(self, event_type, payload):

        if not event_type in self.allowed_event_types:  # only allow listed event types
            logger.info("Cannot publish unrecognized event type {0}.".format(event_type))
            return
        logger.info("Publishing event type {0} to RabbitMQ.".format(event_type))
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=self.routing_key,
                                   body=payload,
                                   properties=pika.BasicProperties(
                                       content_type="application/json",
                                       content_encoding="ascii-8bit",
                                       delivery_mode=2, # for persistence, in case the subscriber crashes, the messages will still be in the queue
                                       message_id=str(uuid.uuid4()),
                                       timestamp=int(round(time.time() * 1000)),
                                       # headers=self.headers,
                                       # correlation_id=self.correlation_id,
                                       # reply_to=self.reply_to,
                                       #
                                       # timestamp=self.timestamp,
                                       # type=self.type,
                                       # user_id=self.user_id,
                                       # app_id=self.app_id
                                   ))
        logger.info("Published event type {0} to RabbitMQ.".format(event_type))

    def close_channel(self):
        if self.channel:
            logger.info("Closing channel.")
            self.channel.close()

    def close_connection(self):
        if self.connection:
            logger.info("Closing connection.")
            self.connection.close()
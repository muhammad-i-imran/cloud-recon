import oslo_messaging
from oslo_config import cfg
import os

from logging_config import Logger

LOGS_FILE_PATH = os.getenv('LOGS_FILE_PATH', '/cloud-reconnoiterer/logs/cloud-reconnoiterer.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

if not LOGS_FILE_PATH:
    raise Exception("Log file is not specified in LOGS_FILE_PATH environment variable. Please specify a valid file path for logging.")

logger = Logger(log_file_path=LOGS_FILE_PATH, log_level=LOG_LEVEL, logger_name=os.path.basename(__file__)).logger


# Available notification list is given in: https://github.com/openstack/nova/blob/master/nova/rpc.py
class NotificationEndpoint(object):
    def __init__(self, event_type, publisher_id, callback):
        self.filter_rule = oslo_messaging.NotificationFilter(
            event_type=event_type,
            publisher_id=publisher_id)
        self.callback = callback  # function is passed here and will be called upon occurence on an event defined in filter_rule

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        self.callback(event_type, payload)


class NotifierStarter(object):
    def __init__(self, transport_url):
        logger.debug("Setting transport URL as %s" % transport_url)
        self.transport_url = transport_url

    def start(self, eventtype_publisherid_tuple_list, exchange_topic_tuple_list, callback):
        """

        :param eventtype_publisherid_tuple_list:
        :param exchange_topic_tuple_list:
        :param callback:
        :return:
        """

        logger.info("Preparing and starting notifications subscriptions.")
        logger.debug("Getting notification transport for transport URL %s." % self.transport_url)
        transport = oslo_messaging.get_notification_transport(cfg.CONF, url=self.transport_url)
        targets = []
        for exchange_topic_tuple in exchange_topic_tuple_list:
            logger.debug("Creating Target for exchange %s and topic %s"% exchange_topic_tuple[0], exchange_topic_tuple[1])
            targets.append(oslo_messaging.Target(exchange=exchange_topic_tuple[0], topic=exchange_topic_tuple[1]))

        endpoints = []
        for eventtype_publisherid_tuple in eventtype_publisherid_tuple_list:
            event_type = eventtype_publisherid_tuple[0]
            publisher_id = eventtype_publisherid_tuple[1]
            logger.debug("Creating NotificationEndpoint for event type %s and publisher id %s"% event_type, publisher_id)
            endpoints.append(NotificationEndpoint(event_type=event_type, publisher_id=publisher_id, callback=callback))
        # pool = "events-listener"
        server = oslo_messaging.get_notification_listener(transport, targets,
                                                          endpoints, executor='threading', allow_requeue=True)
        try:
            logger.info("Starting server for notification listening...")
            server.start()
            logger.info("Waiting for events.")
            server.wait()
        except Exception as ex:
            logger.error("Exception Occured: %s" % str(ex))
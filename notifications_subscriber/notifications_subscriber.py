import oslo_messaging
from oslo_config import cfg


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
        self.transport_url = transport_url

    def start(self, eventtype_publisherid_tuple_list, exchange_topic_tuple_list, callback):
        """

        :param eventtype_publisherid_tuple_list:
        :param exchange_topic_tuple_list:
        :param callback:
        :return:
        """
        transport = oslo_messaging.get_notification_transport(cfg.CONF, url=self.transport_url)
        targets = []
        for exchange_topic_tuple in exchange_topic_tuple_list:
            # targets.append(oslo_messaging.Target(exchange=exchange_topic_tuple[0], topic=exchange_topic_tuple[1]))
            targets.append(oslo_messaging.Target(topic=exchange_topic_tuple[1]))

        endpoints = []
        for eventtype_publisherid_tuple in eventtype_publisherid_tuple_list:
            event_type = eventtype_publisherid_tuple[0]
            publisher_id = eventtype_publisherid_tuple[1]
            endpoints.append(NotificationEndpoint(event_type=event_type, publisher_id=publisher_id, callback=callback))

        # pool = "events-listener"
        server = oslo_messaging.get_notification_listener(transport, targets,
                                                          endpoints, executor='threading', allow_requeue=True)
        print('Starting server...')
        server.start()


        try:
            server.start()
        except Exception as ex:
            print("Exception Occured: %s" % str(ex))
            server.stop()
        finally:
            print("Starting to wait...")
            server.wait()
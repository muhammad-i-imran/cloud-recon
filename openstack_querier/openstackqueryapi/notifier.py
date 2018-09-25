from oslo_config import cfg
import oslo_messaging

### TODO: Refactor the code. add more event types, figure out callback or return a value in case of event occurence.
class NotificationEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        event_type='compute.instance.(create|delete).end',
        publisher_id='^.*')

    def warn(self, ctxt, publisher_id, event_type, payload, metadata):
        print(ctxt)
        print(payload)

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        print(ctxt)
        

        print(event_type)
        print(payload)

class ErrorEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        event_type='^.*$',
        context={'ctxt_key': 'regexp'})

    def error(self, ctxt, publisher_id, event_type, payload, metadata):
        print(payload)

class NotifierStarter(object):
    def __init__(self, transport_url):
        self.transport_url = transport_url
    def start(self):
        transport = oslo_messaging.get_notification_transport(cfg.CONF, url=self.transport_url)
        targets = [
            oslo_messaging.Target(topic='notifications')
        ]
        endpoints = [
            NotificationEndpoint(),
            ErrorEndpoint(),
        ]
        server = oslo_messaging.get_notification_listener(transport, targets,
                                                          endpoints, executor='threading')
        print('Starting server...')
        server.start()
        print('Started server...')
        server.wait()
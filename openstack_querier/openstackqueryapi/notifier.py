from oslo_config import cfg
import oslo_messaging

#TODO: IN-PROGRESS
class NotificationEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        publisher_id='^.*')

    def warn(self, ctxt, publisher_id, event_type, payload, metadata):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
        print(payload)
        print()
    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        print("--------------------------------\n")
        print(payload)

class ErrorEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        event_type='^.*$',
        context={'ctxt_key': 'regexp'})
#        event_type='^instance\..*\.start$',

    def error(self, ctxt, publisher_id, event_type, payload, metadata):
        print("###########################\n")

        print(payload)

def start_notifier(url):
    transport_url = url
    transport = oslo_messaging.get_notification_transport(cfg.CONF, url=transport_url)
    targets = [
        oslo_messaging.Target(topic='notifications')
    ]
    endpoints = [
        NotificationEndpoint(),
        ErrorEndpoint(),
    ]
    pool = "listener-workers"
    server = oslo_messaging.get_notification_listener(transport, targets,
                                                  endpoints, executor='threading')
    print('starting...')
    server.start()
    print('started...')
    server.wait()
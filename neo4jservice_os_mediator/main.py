from multiprocessing.pool import Pool

from event_handlers import *
from notifier import *
from openstack_preprocessor import *
import json
from envvars import *

def begin_all():
    try:
        begin_node_create(cloud_config_info)
    except Exception as ex:
        print("Exception occured: %s" % str(ex))
    try:
        begin_relationship_create(cloud_config_info)
    except Exception as ex: # not needed. but in cases any unexpected problem occurs, then it will not stop the next iterataion
        print("Exception occured: %s" % str(ex))

def main():
    notifier = NotifierStarter(transport_url=NOTIFICATION_TRANSPORT_URL)
    # todo: read it using configuration file instead of env variable
    eventtype_publisherid_tuple_list = [(NOTIFICATION_EVENT_TYPE, NOTIFICATION_PUBLISHER_ID)]
    exchange_topic_tuple_list = [(OPENSTACK_NOTIFICATION_EXCHANGE_NAME, OPENSTACK_NOTIFICATION_TOPIC_NAME),
                                 (DOCKER_NOTIFICATION_EXCHANGE_NAME, DOCKER_NOTIFICATION_TOPIC_NAME)]
    # notifier.start(eventtype_publisherid_tuple_list, exchange_topic_tuple_list, notifier_callback)
    begin_all()

    pool = Pool(processes=5)#todo: get from env
    try:
        pool.apply_async(notifier.start,
                     [eventtype_publisherid_tuple_list, exchange_topic_tuple_list, notifier_callback],
                     None)  # callback is none
        while True:
            # check every TIME_TO_WAIT minutes for the changes (in case notifications are not appearing. but as soon as notifcation appears it will immediatly update graph again.)
            time.sleep(int(TIME_TO_WAIT))
            begin_all()
    except Exception as ex:
        print("Exception occured: %s" % str(ex))
    finally:
        print("Closing pool")
        pool.close()

if __name__ == '__main__':
    NodeManager.NEO4J_SERVICE_URL = RelationshipManager.NEO4J_SERVICE_URL = NEO4J_SERVICE_URL
    configuratons = json.loads(open(CONFIG_FILE_PATH).read())

    cloud_provider = configuratons["cloud_provider"]  ##todo: use this to import modules relevant to the cloud type
    cloud_config_info = configuratons["cloud_config_info"]
    #cloud_config_info = add_prefix_to_dict_keys(cloud_config_info, GRAPH_ELEMENT_TYPE_PREFIX)
    main()
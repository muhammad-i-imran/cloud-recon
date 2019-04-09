import json
from multiprocessing.pool import Pool

from envvars import *
from event_handlers import *
from notifications_subscriber import *
from openstack_preprocessor import *
from logging_config import Logger

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

def begin_all():
    try:
        print("Creating nodes...")
        logger.info("Beggining to create nodes.")
        begin_node_create(cloud_config_info)
    except Exception as ex:
        print("Exception occured while creating nodes: %s" % str(ex))
    try:
        print("Creating relationships...")
        logger.info("Beggining to create relationships for nodes.")
        begin_relationship_create(cloud_config_info)
    except Exception as ex:  # not needed. but in cases any unexpected problem occurs, then it will not stop the next iterataion
        logger.error("Exception occured while creating relationships: %s" % str(ex))

def main():
    logger.debug("Executing notification code.")
    notifier = NotifierStarter(transport_url=NOTIFICATION_TRANSPORT_URL)
    eventtype_publisherid_tuples = []
    for event_type in event_component_mappings:
        eventtype_publisherid_tuples.append(tuple((event_type, event_component_mappings[event_type]['publisher_id'])))

    exchange_topic_tuple_list = [(OPENSTACK_NOTIFICATION_EXCHANGE_NAME, OPENSTACK_NOTIFICATION_TOPIC_NAME),
                                 (DOCKER_NOTIFICATION_EXCHANGE_NAME, DOCKER_NOTIFICATION_TOPIC_NAME)]

    # notifier.start(eventtype_publisherid_tuples, exchange_topic_tuple_list, notifier_callback)
    # print("Begining graph creation")
    # begin_all()

    logger.debug("Creating processes for notification handling.")
    pool = Pool(processes=5)
    try:
        logger.debug("Starting pool for notifications handling.")
        pool.apply_async(notifier.start,
                     [eventtype_publisherid_tuples, exchange_topic_tuple_list, notifier_callback],
                     None)  # callback is none
        while True:
            # check every TIME_TO_WAIT minutes for the changes (in case notifications are not appearing. but as soon as notifcation appears it will immediatly update graph again.)
            begin_all()
            logger.info("Waiting for " + TIME_TO_WAIT + " before the next pass is started.")
            time.sleep(int(TIME_TO_WAIT))
    except Exception as ex:
        logger.error("Exception occured: %s" % str(ex))
    finally:
        logger.info("Closing pool")
        pool.close()

if __name__ == '__main__':
    logger.info("Reading configuration files.")
    NodeManager.NEO4J_SERVICE_URL = RelationshipManager.NEO4J_SERVICE_URL = NEO4J_SERVICE_URL
    configuratons = json.loads(open(CONFIG_FILE_PATH).read())
    cloud_provider = configuratons["cloud_provider"]  ##todo: use this to import modules relevant to the cloud type
    cloud_config_info = configuratons["cloud_config_info"]
    event_component_mappings = json.loads(open(envvars.COMPONENT_EVENT_MAPPING_FILE).read())
    # cloud_config_info = add_prefix_to_dict_keys(cloud_config_info, GRAPH_ELEMENT_TYPE_PREFIX)

    logger.debug("Executing 'main' function.")
    main()
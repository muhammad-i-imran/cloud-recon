import json
import re
import time
from multiprocessing import Pool

from graphelementsdispatcher.node_manager import NodeManager
from graphelementsdispatcher.relationship_manager import RelationshipManager
from osquerieshandler.osqueriers import *
from utils import *
from notifier import *
from event_handlers import *
from openstack_preprocessor import *



def begin_all():
    try:
        begin_node_create()
        # if node creation is asynch, then wait until all nodes are created.
        begin_relationship_create()
    except Exception as e:
        print("Exception occured: " + str(e))
        pass

def main():
    notifier = NotifierStarter(transport_url=NOTIFICATION_TRANSPORT_URL)
    notifier.start(NOTIFICATION_EVENT_TYPE, NOTIFICATION_PUBLISHER_ID, NOTIFICATION_TOPIC_NAME, notifier_callback)
    begin_all()

    ## the following code is commenting only for dev env
    # pool = Pool(processes=2)#todo: get from env
    # pool.apply_async(notifier.start,
    #                  [NOTIFICATION_EVENT_TYPE, NOTIFICATION_PUBLISHER_ID, NOTIFICATION_TOPIC_NAME, notifier_callback],
    #                  notifier_callback)  # callback is none
    # while True:
    #     # check every TIME_TO_WAIT minutes for the changes (in case notifications are not appearing. but as soon as notifcation appears it will immediatly update graph again.)
    #     time.sleep(int(TIME_TO_WAIT))
    #     begin_all()




if __name__ == '__main__':
    NodeManager.NEO4J_SERVICE_URL = RelationshipManager.NEO4J_SERVICE_URL = NEO4J_SERVICE_URL
    configuratons = json.loads(open(CONFIG_FILE_PATH).read())
    cloud_provider = configuratons["cloud_provider"] ##todo: use this to import modules relevant to the cloud type
    cloud_config_info = configuratons["cloud_config_info"]
    cloud_config_info = add_prefix_to_dict_keys(cloud_config_info, GRAPH_ELEMENT_TYPE_PREFIX)
    main()
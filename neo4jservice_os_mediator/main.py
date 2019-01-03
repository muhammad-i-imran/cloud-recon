import json
import re
import time

from multiprocessing import Pool
from node_manager import NodeManager
from openstackqueryapi import NotifierStarter
from osqueriers import *
from relationship_manager import RelationshipManager
from collections import namedtuple
from flatten_json import flatten
from utils import *

#todo: move provider-dependent functionality in seperate file, so it can be generalized later
def create_servers(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getServers(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_containers(node_type):
    openstack_info[node_type]["data"] = NodeManager.create_containers_nodes(node_type=node_type,
                                                                            server_name_attr=openstack_info["SERVERS"][
                                                                                "name_attr"],
                                                                            openstack_info=openstack_info,
                                                                            private_keys_folder=PRIVATE_KEYS_FOLDER,
                                                                            nova_querier=novaQuerier,
                                                                            vm_username=VM_USERNAME)


def create_host_aggregates(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getHostAggregates(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_availability_zones(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getAvailabilityZones(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_services(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getServices(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_hypervisors(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getHypervisors(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_flavors(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getFlavors(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_volumes(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=cinderQuerier.getVolumes(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_key_pairs(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=novaQuerier.getKeyPairs(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_images(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=glanceQuerier.getImages(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_networks(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=neutronQuerier.getNetworks(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_subnets(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=neutronQuerier.getSubNets(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_routers(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=neutronQuerier.getRouters(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])


def create_users(node_type):
    openstack_info[node_type]["data"] = NodeManager.prepare_node_data(data_list=keystoneQuerier.getUsers(),
                                                                     node_type=node_type,
                                                                     # label_key=openstack_info[node_type]["name_attr"],
                                                                     id_key=openstack_info[node_type]["id_key"])

def not_supported():
    raise Exception("Not supported yet.")


def create_graph_elements(element_type):
    switcher = {
        "SERVERS": create_servers,
        "HOST_AGGREGATES": create_host_aggregates,
        "AVAILABILITY_ZONES": create_availability_zones,
        "SERVICES": create_services,
        "HYPERVISORS": create_hypervisors,
        "FLAVORS": create_flavors,
        "VOLUMES": create_volumes,
        "KEY_PAIRS": create_key_pairs,
        "IMAGES": create_images,
        "NETWORKS": create_networks,
        "SUBNETS": create_subnets,
        "ROUTERS": create_routers,
        "CONTAINERS": create_containers,
        "USERS": create_users
    }
    func = switcher.get(element_type, lambda: not_supported)
    return func

def begin_node_create():
    nodes = list(openstack_info.keys())
    nodes.remove("CONTAINERS")

    for node_type in nodes:
        create_graph_elements(node_type)(node_type)

    # for container (because it depends on SERVERS)
    try:
        create_graph_elements("CONTAINERS")("CONTAINERS")
    except Exception as e:
        print("Exception occured: " + str(e))
        pass

def begin_relationship_create():
    for key in openstack_info:
        source_node_type = key
        relationships_info = openstack_info[key]["RELATIONSHIPS"]
        data = openstack_info[key]["data"] ##TODO:  get rid of the data. and fetch at runtime
        for relationship in relationships_info:
            NodeRelationshipAttrsMappingInfo = namedtuple("NodeRelationshipAttrsMappingInfo",
                                                          "source_attr_name is_source_attr_name_regex target_node_type target_node_attr_name is_target_attr_name_regex target_value_data_type relationship_name relationship_attrs")
            NodeRelationshipAttrsMappingInfo = NodeRelationshipAttrsMappingInfo(
                source_attr_name=relationship["source_attr_name"],
                is_source_attr_name_regex=relationship["is_source_attr_name_regex"],
                target_node_type=relationship["target_node_type"],
                target_node_attr_name=relationship["target_node_attr_name"],
                is_target_attr_name_regex=relationship["is_target_attr_name_regex"],
                target_value_data_type=relationship["target_value_data_type"],
                relationship_name=relationship["relationship_name"],
                relationship_attrs=relationship["relationship_attrs"])

            for d in data:
                if NodeRelationshipAttrsMappingInfo.is_source_attr_name_regex:
                    source_keys = list(filter(re.compile(NodeRelationshipAttrsMappingInfo.source_attr_name).match,
                                              d.node_attributes.__dict__.keys()))
                    for k in source_keys:
                        RelationshipManager.createRelationships(
                            source_node_attr_name=k,
                            target_node_attr_name=NodeRelationshipAttrsMappingInfo.target_node_attr_name,
                            source_node_attr_value=d.node_attributes.__dict__[k],
                            source_node_type=source_node_type,
                            target_node_type=NodeRelationshipAttrsMappingInfo.target_node_type,
                            relationship=NodeRelationshipAttrsMappingInfo.relationship_name,
                            relationship_attributes_dict=NodeRelationshipAttrsMappingInfo.relationship_attrs)
                else:
                    RelationshipManager.createRelationships(
                        source_node_attr_name=NodeRelationshipAttrsMappingInfo.source_attr_name,
                        target_node_attr_name=NodeRelationshipAttrsMappingInfo.target_node_attr_name,
                        source_node_attr_value=d.node_attributes.__dict__[
                            NodeRelationshipAttrsMappingInfo.source_attr_name],
                        source_node_type=source_node_type,
                        target_node_type=NodeRelationshipAttrsMappingInfo.target_node_type,
                        relationship=NodeRelationshipAttrsMappingInfo.relationship_name,
                        relationship_attributes_dict=NodeRelationshipAttrsMappingInfo.relationship_attrs)

def begin_all():
    try:
        begin_node_create()
        begin_relationship_create()
    except Exception as e:
        print("Exception occured: " + str(e))
        pass

def notifier_callback(event_type, payload):
    # TODO: Compare graph data with openstack data and update node if different
    openstack_component = NodeManager.get_node_by_attribute('id', payload['id']) # get openstack node data using apis
    openstack_component_flattened_dict = flatten(openstack_component, separator="___")
    openstack_component_neo4j = NodeManager.get_node_by_attribute('id', payload['id']) # will receive data that is already flattened when inserted
    if not diff_dictionaries(openstack_component_neo4j, openstack_component_flattened_dict): # if dictionaries are different then update, otherwise ignore
      NodeManager.update_node()

def main():
    notifier = NotifierStarter(transport_url=NOTIFICATION_TRANSPORT_URL)
    notifier.start(NOTIFICATION_EVENT_TYPE, NOTIFICATION_PUBLISHER_ID, NOTIFICATION_TOPIC_NAME, notifier_callback)
    begin_all()

    ## the following code is commenting only for dev env
    # pool = Pool(processes=2)
    # pool.apply_async(notifier.start,
    #                  [NOTIFICATION_EVENT_TYPE, NOTIFICATION_PUBLISHER_ID, NOTIFICATION_TOPIC_NAME, notifier_callback],
    #                  notifier_callback)  # callback is none
    #
    # while True:
    #     begin_all()
    #     # check every TIME_TO_WAIT minutes for the changes (in case notifications are not appearing. but as soon as notifcation appears it will immediatly update graph again.)
    #     print("###################################################################################")
    #     time.sleep(int(TIME_TO_WAIT))

if __name__ == '__main__':
    NodeManager.NEO4J_SERVICE_URL = RelationshipManager.NEO4J_SERVICE_URL = NEO4J_SERVICE_URL
    openstack_info = json.loads(open(CONFIG_FILE_PATH).read())
    main()
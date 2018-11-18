import json
import re
import time

from multiprocessing import Pool
from nodecreator import NodeCreator
from openstackqueryapi import NotifierStarter
from osqueriers import *
from relationshipcreator import RelationshipCreator


# TODO: Refactor the Code


def create_servers(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getServers(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])

def create_containers(node_type):
    openstack_info[node_type]["data"] = NodeCreator.create_containers_nodes(node_type, openstack_info, PRIVATE_KEY_PATH, novaQuerier, VM_USERNAME)


def create_host_aggregates(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getHostAggregates(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_availability_zones(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getAvailabilityZones(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_services(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getServices(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_hypervisors(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getHypervisors(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_flavors(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getFlavors(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_volumes(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=cinderQuerier.getVolumes(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_key_pairs(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getKeyPairs(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_images(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=glanceQuerier.getImages(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_networks(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=neutronQuerier.getNetworks(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_subnets(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=neutronQuerier.getSubNets(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


def create_routers(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=neutronQuerier.getRouters(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])


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
        "CONTAINERS": create_containers
    }
    func = switcher.get(element_type, lambda: not_supported)
    return func


# think of a good name for this function
def begin_node_create():
    nodes = list(openstack_info.keys())
    nodes.remove("CONTAINERS")
    for node_type in nodes:
        create_graph_elements(node_type)(node_type)

    #for container (because it depends on SERVERS)
    try:
        create_graph_elements("CONTAINERS")("CONTAINERS")
    except:
        pass

    # for key in openstack_info.keys():
    #     print(key)
    #     for d in openstack_info[key]["data"]:
    #         print(d.__dict__["name"] + ":" + str(d.__dict__["node_attributes"].__dict__))


# think of a good name for this function
def begin_relationship_create():
    for key in openstack_info:
        source_node_type = key
        info = openstack_info[key]
        name_attr = "name"

        relationships_info = openstack_info[key]["RELATIONSHIPS"]
        data = openstack_info[key]["data"]
        print("KEY: " + key)
        for relationship in relationships_info:
            source_attr_name = relationship["source_attr_name"]
            is_source_attr_name_regex = relationship["is_source_attr_name_regex"]
            target_node_type = relationship["target_node_type"]
            target_node_attr_name = relationship["target_node_attr_name"]
            is_target_attr_name_regex = relationship["is_target_attr_name_regex"]
            target_value_data_type = relationship["target_value_data_type"]
            relationship_name = relationship["relationship_name"]
            relationship_attrs = relationship["relationship_attrs"]

            for d in data:
                if is_source_attr_name_regex:
                    source_keys = list(filter(re.compile(source_attr_name).match, d.node_attributes.__dict__.keys()))
                    print(source_keys)
                    for key in source_keys:
                        RelationshipCreator.createRelationships(source_node_attr_name=name_attr,
                                                                target_node_attr_name=target_node_attr_name,
                                                                source_node_attr_value=d.name,
                                                                target_node_attr_value=d.node_attributes.__dict__[key],
                                                                source_node_type=source_node_type,
                                                                target_node_type=target_node_type,
                                                                relationship=relationship_name,
                                                                relationship_attributes_dict=relationship_attrs,
                                                                is_source_attr_name_regex=is_source_attr_name_regex,
                                                                is_target_attr_name_regex=is_target_attr_name_regex)
                else:
                    RelationshipCreator.createRelationships(source_node_attr_name=name_attr,
                                                            target_node_attr_name=target_node_attr_name,
                                                            source_node_attr_value=d.name,
                                                            target_node_attr_value=d.node_attributes.__dict__[
                                                                source_attr_name],
                                                            source_node_type=source_node_type,
                                                            target_node_type=target_node_type,
                                                            relationship=relationship_name,
                                                            relationship_attributes_dict=relationship_attrs,
                                                            is_source_attr_name_regex=is_source_attr_name_regex,
                                                            is_target_attr_name_regex=is_target_attr_name_regex)




def begin_all():
    try:
        begin_node_create()
        begin_relationship_create()
    except:
        pass


def dummy_callback():
    print("dummy callback")


def notifier_callback():
    begin_all()


def main():
    notifier = NotifierStarter(transport_url=NOTIFICATION_TRANSPORT_URL)

    pool = Pool(processes=1)
    pool.apply_async(notifier.start,
                     [NOTIFICATION_EVENT_TYPE, NOTIFICATION_PUBLISHER_ID, NOTIFICATION_TOPIC_NAME, notifier_callback],
                     None)

    while True:
        begin_all()
        time.sleep(
            int(
                TIME_TO_WAIT))  # check every TIME_TO_WAIT minutes for the changes (in case notifications are not appearing. but as soon as notifcation appears it will immediatly update graph again.)


if __name__ == '__main__':
    NodeCreator.NEO4J_SERVICE_URL = RelationshipCreator.NEO4J_SERVICE_URL = NEO4J_SERVICE_URL
    openstack_info = json.loads(open(CONFIG_FILE_PATH).read())
    main()

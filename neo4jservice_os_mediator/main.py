import json
import os
import re
import time

from nodecreator import NodeCreator
from openstackqueryapi.queryos import *
from relationshipcreator import RelationshipCreator
from openstackqueryapi.notifier import *

# TODO: Refactor the Code

NodeCreator.NEO4J_SERVICE_URL = RelationshipCreator.NEO4J_SERVICE_URL = os.getenv('NEO4J_SERVICE_URL',
                                                                                  'http://localhost:15135/neo4j')  # config.SERVICE_URL
OS_AUTH_URL = os.getenv('OS_AUTH_URL', "http://x.x.x.x:5000")
OS_USERNAME = os.getenv('OS_USERNAME', "xxxxxxxxxxxxxxxxxxx")
OS_PASSWORD = os.getenv('OS_PASSWORD', "xxxxxxxxxxxxxxxxxxxxx")
OS_PROJECT_ID = os.getenv('OS_TENANT_ID', "xxxxxxxxxxxxxxxxxxxxxxx")
OS_API_VERSION = os.getenv('OS_API_VERSION', "2.0")
NOTIFICATION_TRANSPORT_URL = os.getenv('NOTIFICATION_TRANSPORT_URL', "rabbit://openstack:xxxxx@x.x.x.x:5672")
PRIVATE_KEY = os.getenv('PRIVATE_KEY', """-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----""")


def getOpenstackConnection(auth_url, username, password, project_id, version):
    return OpenstackConnector(auth_url=auth_url, username=username, password=password, project_id=project_id,
                              version=version)


conn = getOpenstackConnection(auth_url=OS_AUTH_URL, username=OS_USERNAME, password=OS_PASSWORD,
                              project_id=OS_PROJECT_ID, version=OS_API_VERSION)

###################################################################################

novaQuerier = NovaQuerier(conn)
novaQuerier.connect()

glanceQuerier = GlanceQuerier(conn)
glanceQuerier.connect()

neutronQuerier = NeutronQuerier(conn)
neutronQuerier.connect()

cinderQuerier = CinderQuerier(conn)
cinderQuerier.connect()


###################################################################################

def readJsonFile(file_name):
    openstack_info_file = open(file_name)
    openstack_info_str = openstack_info_file.read()
    return json.loads(openstack_info_str)


config_file_path = os.getenv('CONFIG_FILE_PATH', 'openstack_info.json')
openstack_info = readJsonFile(config_file_path)


####################################################################################################
def create_servers(node_type):
    openstack_info[node_type]["data"] = NodeCreator.prepareNodesData(data_list=novaQuerier.getServers(),
                                                                     node_type=node_type,
                                                                     label_key=openstack_info[node_type]["name_attr"],
                                                                     id_keys=openstack_info[node_type]["id_keys"])
    create_containers("CONTAINERS")


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


def create_containers(node_type):
    command = "sudo docker ps --format \"table {{.ID}}|{{.Names}}|{{.Image}}\""
    for s in openstack_info["SERVERS"]["data"]:
        server_id = s.node_attributes.__dict__["id"]
        server = novaQuerier.getServer(server_id)

        vmSshQuerier = CustomVirtualMachineQuerier()
        ip = server.addresses["neo4j-private"][1]["addr"]
        username = 'ubuntu'
        private_key_content = PRIVATE_KEY
        vmSshQuerier.connect(ip=ip, username=username, private_key_content=private_key_content)

        stdin, stdout, stderr = vmSshQuerier.executeCommandOnVM(command)
        containers_string_info = stdout.readlines()[1:]
        containers_list = []
        for c in containers_string_info:
            container_info_dict = {}
            container_info = re.split(r'|', c)
            container_info_dict["id"] = container_info[0]
            container_info_dict["container_name"] = container_info[1]
            container_info_dict["image_name"] = container_info[2]
            container_info_dict["server_name"] = s.name
            container_info_dict["server_id"] = server_id
            containers_list.append(container_info_dict)

        print(containers_list)
        NodeCreator.prepareNodesData(data_list=containers_list, node_type=node_type, label_key="image_name",
                                     id_keys=["id"])
        vmSshQuerier.closeConnection()


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
        "ROUTERS": create_routers
    }
    func = switcher.get(element_type, lambda: not_supported)
    return func


# think of a good name for this function
def begin_node_create():
    for node_type in openstack_info.keys():
        create_graph_elements(node_type)(node_type)

    for key in openstack_info.keys():
        print(key)
        for d in openstack_info[key]["data"]:
            print(d.__dict__["name"] + ":" + str(d.__dict__["node_attributes"].__dict__))


# think of a good name for this function
def begin_relationship_create():
    for key in openstack_info:
        source_node_type = key
        info = openstack_info[key]
        name_attr = "name"

        relationships_info = openstack_info[key]["RELATIONSHIPS"]
        data = openstack_info[key]["data"]
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
    begin_node_create()
    begin_relationship_create()

def callback_func():
    print("callback...")
    begin_all()

def main():
    notifier = NotifierStarter(transport_url=NOTIFICATION_TRANSPORT_URL)
    notifier.start(event_type='^.*?.end$', publisher_id='^.*', callback=callback_func)

    while True:
        begin_all()
        time.sleep(600)  # check every 10 minutes for the changes (in case notifications are not appearing. but as soon as notifcation appears it will immediatly update graph again.)

if __name__ == '__main__':
    main()

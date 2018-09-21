from flatten_json import flatten
from openstackqueryapi.queryos import *
from graphserviceschema.serviceschema import *
from mediator.caller import *
import json
import re
import time
import os

# TODO: Refactor the Code

NEO4J_SERVICE_URL = os.getenv('NEO4J_SERVICE_URL', 'http://localhost:5000/neo4j') # config.SERVICE_URL
OS_AUTH_URL = os.getenv('OS_AUTH_URL', "http://0.0.0.0:5000/v2.0")
OS_USERNAME = os.getenv('OS_USERNAME', "")
OS_PASSWORD = os.getenv('OS_PASSWORD', "")
OS_PROJECT_ID = os.getenv('OS_TENANT_ID', "")
OS_API_VERSION = os.getenv('OS_API_VERSION', "2.0")
PRIVATE_KEY = os.getenv('PRIVATE_KEY', """-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----""")



def getOpenstackConnection():
    conn = OpenstackConnector(auth_url=OS_AUTH_URL, username=OS_USERNAME, password=OS_PASSWORD,
                              project_id=OS_PROJECT_ID, version=OS_API_VERSION)
    return conn

conn = getOpenstackConnection()

novaQuerier = NovaQuerier(conn)
novaQuerier.connect()

glanceQuerier = GlanceQuerier(conn)
glanceQuerier.connect()

neutronQuerier = NeutronQuerier(conn)
neutronQuerier.connect()

cinderQuerier = CinderQuerier(conn)
cinderQuerier.connect()


def createNode(id_keys, label, node_type, node_attrributtes_dict):
    node_attributes = NodeAttributes(node_attrributtes_dict)
    node = Node(id_keys=id_keys, name=label, node_type=node_type, node_attributes=node_attributes)
    data = node.toJSON()
    callServicePost(url=NEO4J_SERVICE_URL + "/nodes/create_node", data=data.replace("\n", ""))
    return node


def prepareNodesData(list, node_type, label_key="name", id_keys=["id"]):
    nodes = []
    for i in list:
        info = i if type(i) is dict else i.__dict__
        # id = info[id_key]

        # info["id"] = info[id_key]
        label = info.pop(label_key, None)

        flatten_info_dict = flatten(info, separator="___")
        node = createNode(id_keys, label, node_type, flatten_info_dict)
        nodes.append(node)
    return nodes


def createRelationships(source_node_attr_name, target_node_attr_name,
                        source_node_attr_value, target_node_attr_value, source_node_type,
                        target_node_type, relationship, relationship_attributes_dict, is_source_attr_name_regex,
                        is_target_attr_name_regex):
    relationship_attributes = RelationshipAttributes(relationship_attributes_dict)

    relationship = Relationship(source_node_attr_name=source_node_attr_name,
                                target_node_attr_name=target_node_attr_name,
                                source_node_attr_value=source_node_attr_value,
                                target_node_attr_value=target_node_attr_value,
                                source_node_type=source_node_type,
                                target_node_type=target_node_type, relationship=relationship,
                                relationship_attributes=relationship_attributes,
                                is_source_attr_name_regex=is_source_attr_name_regex,
                                is_target_attr_name_regex=is_target_attr_name_regex)
    data = relationship.toJSON()
    callServicePost(url=NEO4J_SERVICE_URL + "/relationships/create_relationship", data=data.replace("\n", ""))


def readJsonFile(file_name):
    openstack_info_file = open(file_name)
    openstack_info_str = openstack_info_file.read()
    return json.loads(openstack_info_str)


config_file_path = os.getenv('CONFIG_FILE_PATH', 'openstack_info.json')
openstack_info = readJsonFile(config_file_path)
####################################################################################################
def create_servers(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getServers(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])
    create_containers("CONTAINERS")


def create_host_aggregates(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getHostAggregates(), key,
                                                   openstack_info[key]["name_attr"], openstack_info[key]["id_keys"])


def create_availability_zones(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getAvailabilityZones(), key,
                                                   openstack_info[key]["name_attr"], openstack_info[key]["id_keys"])


def create_services(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getServices(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_hypervisors(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getHypervisors(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_flavors(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getFlavors(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_volumes(key):
    openstack_info[key]["data"] = prepareNodesData(cinderQuerier.getVolumes(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_key_pairs(key):
    openstack_info[key]["data"] = prepareNodesData(novaQuerier.getKeyPairs(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_images(key):
    openstack_info[key]["data"] = prepareNodesData(glanceQuerier.getImages(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_networks(key):
    openstack_info[key]["data"] = prepareNodesData(neutronQuerier.getNetworks(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_subnets(key):
    openstack_info[key]["data"] = prepareNodesData(neutronQuerier.getSubNets(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])


def create_routers(key):
    openstack_info[key]["data"] = prepareNodesData(neutronQuerier.getRouters(), key, openstack_info[key]["name_attr"],
                                                   openstack_info[key]["id_keys"])

def create_containers(key):
    command = "sudo docker ps --format \"table {{.ID}}|{{.Names}}|{{.Image}}\""
    for s in openstack_info["SERVERS"]["data"]:
        server_id=s.node_attributes.__dict__["id"]
        server = novaQuerier.getServer(server_id)

        vmSshQuerier = CustomVirtualMachineQuerier()
        ip = server.addresses["neo4j-private"][1]["addr"]
        username = 'ubuntu'
        private_key_content = PRIVATE_KEY
        vmSshQuerier.connect(ip=ip, username=username, private_key_content=private_key_content)

        stdin, stdout, stderr = vmSshQuerier.executeCommandOnVM(command)
        containers_string_info = stdout.readlines()[1:]
        containers_list=[]
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
        prepareNodesData(containers_list, key, label_key="image_name", id_keys=["id"])
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

while True:
    for key in openstack_info.keys():
        create_graph_elements(key)(key)

    for key in openstack_info.keys():
        print(key)
        for d in openstack_info[key]["data"]:
            print(d.__dict__["name"] + ":" + str(d.__dict__["node_attributes"].__dict__))

    ####################################################################################################

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
                        createRelationships(source_node_attr_name=name_attr, target_node_attr_name=target_node_attr_name,
                                            source_node_attr_value=d.name,
                                            target_node_attr_value=d.node_attributes.__dict__[key],
                                            source_node_type=source_node_type, target_node_type=target_node_type,
                                            relationship=relationship_name, relationship_attributes_dict=relationship_attrs,
                                            is_source_attr_name_regex=is_source_attr_name_regex,
                                            is_target_attr_name_regex=is_target_attr_name_regex)
                else:
                    createRelationships(source_node_attr_name=name_attr, target_node_attr_name=target_node_attr_name,
                                        source_node_attr_value=d.name,
                                        target_node_attr_value=d.node_attributes.__dict__[source_attr_name],
                                        source_node_type=source_node_type, target_node_type=target_node_type,
                                        relationship=relationship_name, relationship_attributes_dict=relationship_attrs,
                                        is_source_attr_name_regex=is_source_attr_name_regex,
                                        is_target_attr_name_regex=is_target_attr_name_regex)


    time.sleep(300)
from flatten_json import flatten
from openstackqueryapi.queryos import *
from graphserviceschema.serviceschema import *
from mediator.caller import *
import collections

# def flatten(d, parent_key='', sep='>'):
#     items = []
#     for k, v in d.items():
#         new_key = parent_key + sep + k if parent_key else k
#         if isinstance(v, collections.MutableMapping):
#             items.extend(flatten(v, new_key, sep=sep).items())
#         else:
#             items.append((new_key, v))
#     return dict(items)

NEO4J_SERVICE_URL = "http://localhost:5000/neo4j"

def getOpenstackConnection():
    conn = OpenstackConnector(auth_url="http://130.149.249.252:5000/v2.0", username="muhammad", password="CIT123456",
                              project_id="e326f15678674e3cbc83097659171e8f", version="2.0")
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


def createNode(label, node_type, node_attrributtes_dict):
    node_attributes = NodeAttributes(node_attrributtes_dict)
    node = Node(label=label, node_type=node_type, node_attributes=node_attributes)
    data = node.toJSON()
    callServicePost(url=NEO4J_SERVICE_URL + "/nodes/create_node", data=data.replace("\n", ""))
    return node


def novaNodes(list, node_type, label_key="name"):
    nodes = []
    for i in list:
        info = i if type(i) is dict else i.__dict__ #["_info"]
        label = info.pop(label_key, None)
        flatten_info_dict = flatten(info, separator=".")
        node = createNode(label, node_type, flatten_info_dict)
        nodes.append(node)

    return nodes

def createRelationships(first_node, second_node, first_node_type, second_node_type, relationship, relationship_attributes_dict, ):
    relationship_attributes = RelationshipAttributes(relationship_attributes_dict)
    relationship = Relationship(first_node, second_node, first_node_type,
                                second_node_type, relationship, relationship_attributes)
    data = relationship.toJSON()
    callServicePost(url=NEO4J_SERVICE_URL + "/relationships/create_relationship", data=data.replace("\n", ""))


# openstack_structure= {"server": { "depends_on": {}}}

name_labels = { "SERVERS":"name", "HOST_AGGREGATES":"name", "AVAILABILITY_ZONES":"zoneName", "SERVICES":"binary", "HYPERVISORS":"hypervisor_hostname", "FLAVORS":"name", "VOLUMES":"name", "KEY_PAIRS":"name", "IMAGES":"name", "NETWORKS":"name", "SUBNETS":"name", "ROUTERS":"name"}

servers_data=novaNodes(novaQuerier.getServers(), "SERVERS", name_labels["SERVERS"])
host_aggregates_data=novaNodes(novaQuerier.getHostAggregates(), "HOST_AGGREGATES", name_labels["HOST_AGGREGATES"])
availabilty_zones_data=novaNodes(novaQuerier.getAvailabilityZones(), "AVAILABILITY_ZONES", name_labels["AVAILABILITY_ZONES"])
binary_data=novaNodes(novaQuerier.getServices(), "SERVICES", name_labels["SERVICES"])
hypervisors_data=novaNodes(novaQuerier.getHypervisors(), "HYPERVISORS", name_labels["HYPERVISORS"])
flavors_data=novaNodes(novaQuerier.getFlavors(), "FLAVORS", name_labels["FLAVORS"])

##
volumes_data=novaNodes(cinderQuerier.getVolumes(), "VOLUMES", name_labels["VOLUMES"])
keypairs_data=novaNodes(novaQuerier.getKeyPairs(), "KEY_PAIRS", name_labels["KEY_PAIRS"])

images_data=novaNodes(glanceQuerier.getImages(), "IMAGES", name_labels["IMAGES"])
networks_data=novaNodes(neutronQuerier.getNetworks(), "NETWORKS", name_labels["NETWORKS"])
subnetworks_data=novaNodes(neutronQuerier.getSubNets(), "SUBNETS", name_labels["SUBNETS"])
routers_data=novaNodes(neutronQuerier.getRouters(), "ROUTERS", name_labels["ROUTERS"])

## more components


#####################################################################################################
##CREATE RELATIONSHIPS
server_relationship_attrs = {"OS-EXT-AZ:availability_zone":"AVAILABILITY_ZONES", "OS-EXT-SRV-ATTR:hypervisor_hostname":"HYPERVISORS"}
for server in servers_data:
    for i in server_relationship_attrs.keys():
        createRelationships(server.label, server.node_attributes.__dict__[i], "SERVERS", server_relationship_attrs[i], "RUNS_ON", {"STATUS":"ACTIVE"})


# for i in neutronQuerier.getNetworks():
#     network = i
#     label = network.pop("name", None)
#     node_type = "NETWORK"
#     node_attributes = NodeAttributes(flatten(network, separator="."))
#     node = Node(label=label, node_type=node_type, node_attributes=node_attributes)
#     data = node.toJSON()
#     callServicePost(url=NEO4J_SERVICE_URL + "/nodes/create_node", data=data.replace("\n", ""))

# for i in glanceQuerier.getImages():
#     image = i.__dict__['__original__']
#     label = image.pop("name", None)
#     node_type = "IMAGE"
#     node_attributes = NodeAttributes(flatten(image, separator="."))
#     node = Node(label=label, node_type=node_type, node_attributes=node_attributes)
#     data = node.toJSON()
#     callServicePost(url=NEO4J_SERVICE_URL + "/nodes/create_node", data=data.replace("\n", ""))
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44
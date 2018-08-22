from flatten_json import flatten
from openstackqueryapi.queryos import *
from graphserviceschema.serviceschema import *
from mediator.caller import *


#TODO: Refactor the Code

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
    node = Node(name=label, node_type=node_type, node_attributes=node_attributes)
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

def createRelationships(first_node, second_node, first_node_attr, second_node_attr, first_node_type, second_node_type, relationship, relationship_attributes_dict, ):
    relationship_attributes = RelationshipAttributes(relationship_attributes_dict)
    relationship = Relationship(first_node, second_node, first_node_attr, second_node_attr,first_node_type,
                                second_node_type, relationship, relationship_attributes)
    data = relationship.toJSON()
    callServicePost(url=NEO4J_SERVICE_URL + "/relationships/create_relationship", data=data.replace("\n", ""))



name_labels = { "SERVERS":"name", "HOST_AGGREGATES":"name", "AVAILABILITY_ZONES":"zoneName", "SERVICES":"binary", "HYPERVISORS":"hypervisor_hostname", "FLAVORS":"name", "VOLUMES":"name", "KEY_PAIRS":"name", "IMAGES":"name", "NETWORKS":"name", "SUBNETS":"name", "ROUTERS":"name"}

####################################################################################################
def create_servers():
    return novaNodes(novaQuerier.getServers(), "SERVERS", name_labels["SERVERS"])

def create_host_aggregates():
    return novaNodes(novaQuerier.getHostAggregates(), "HOST_AGGREGATES", name_labels["HOST_AGGREGATES"])

def create_availability_zones():
    return novaNodes(novaQuerier.getAvailabilityZones(), "AVAILABILITY_ZONES", name_labels["AVAILABILITY_ZONES"])

def create_services():
    return novaNodes(novaQuerier.getServices(), "SERVICES", name_labels["SERVICES"])

def create_hypervisors():
    return novaNodes(novaQuerier.getHypervisors(), "HYPERVISORS", name_labels["HYPERVISORS"])

def create_flavors():
    return novaNodes(novaQuerier.getFlavors(), "FLAVORS", name_labels["FLAVORS"])

def create_volumes():
    return novaNodes(cinderQuerier.getVolumes(), "VOLUMES", name_labels["VOLUMES"])

def create_key_pairs():
    return novaNodes(novaQuerier.getKeyPairs(), "KEY_PAIRS", name_labels["KEY_PAIRS"])

def create_images():
    return novaNodes(glanceQuerier.getImages(), "IMAGES", name_labels["IMAGES"])

def create_networks():
    return novaNodes(neutronQuerier.getNetworks(), "NETWORKS", name_labels["NETWORKS"])

def create_subnets():
    return novaNodes(neutronQuerier.getSubNets(), "SUBNETS", name_labels["SUBNETS"])

def create_routers():
    return novaNodes(neutronQuerier.getRouters(), "ROUTERS", name_labels["ROUTERS"])

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



for key in name_labels.keys():
    create_graph_elements(key)()


####################################################################################################

# openstack_structure= {"server": { "depends_on": {}}}
"""
{
"SERVERS": {
"name_attr":"name"
"RELATIONSHIPS": [{"attr_name": "OS-EXT-AZ:availability_zone", "target_node_type":"AVAILABILITY_ZONES", "target_node_attr_name":"name" ,"target_value_data_type":"string"}, {...}]
},
"ROUTERS": {
"name_attr":"name"
"RELATIONSHIPS": [{"attr_name": "external_gateway_info.network_id", "target_node_type":"NETWORKS", "target_node_attr_name":"id" ,"target_value_data_type":"string"}, 
                {"attr_name": "external_gateway_info.external_fixed_ips.0.subnet_id", "target_node_type":"SUBNETS", "target_node_attr_name":"id" ,"target_value_data_type":"string"}
]
},
}
"""
#
#
# #####################################################################################################
# ##CREATE RELATIONSHIPS
# relationship_attrs = {"SERVERS":{"OS-EXT-AZ:availability_zone":"AVAILABILITY_ZONES", "OS-EXT-SRV-ATTR:hypervisor_hostname":"HYPERVISORS"}, "ROUTERS": {"external_gateway_info.network_id": "NETWORKS", "external_gateway_info.external_fixed_ips.0.subnet_id":"SUBNETS"}}
#
# for i in relationship_attrs.keys():
#     for j in relationship_attrs[i].keys():
#         if i == "SERVERS":
#             for server in servers_data:
#                 createRelationships(server.label, server.node_attributes.__dict__[j], "name", "name", i, relationship_attrs[i][j], "RUNS_ON", {"STATUS":"ACTIVE"})
#         elif i == "ROUTERS":
#             for router in routers_data:
#                 createRelationships(router.label, router.node_attributes.__dict__[j], "name", "id", i, relationship_attrs[i][j], "RUNS_ON", {"STATUS":"ACTIVE"})
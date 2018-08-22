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

def createRelationships(first_node, second_node, first_node_attr, second_node_attr, first_node_type, second_node_type, relationship, relationship_attributes_dict, ):
    relationship_attributes = RelationshipAttributes(relationship_attributes_dict)
    relationship = Relationship(first_node, second_node, first_node_attr, second_node_attr,first_node_type,
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
relationship_attrs = {"SERVERS":{"OS-EXT-AZ:availability_zone":"AVAILABILITY_ZONES", "OS-EXT-SRV-ATTR:hypervisor_hostname":"HYPERVISORS"}, "ROUTERS": {"external_gateway_info.network_id": "NETWORKS", "external_gateway_info.external_fixed_ips.0.subnet_id":"SUBNETS"}}

for i in relationship_attrs.keys():
    for j in relationship_attrs[i].keys():
        if i == "SERVERS":
            for server in servers_data:
                createRelationships(server.label, server.node_attributes.__dict__[j], "name", "name", i, relationship_attrs[i][j], "RUNS_ON", {"STATUS":"ACTIVE"})
        elif i == "ROUTERS":
            for router in routers_data:
                createRelationships(router.label, router.node_attributes.__dict__[j], "name", "id", i, relationship_attrs[i][j], "RUNS_ON", {"STATUS":"ACTIVE"})
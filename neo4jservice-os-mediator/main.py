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

def prepareNodesData(list, node_type, label_key="name"):
    nodes = []
    for i in list:
        info = i if type(i) is dict else i.__dict__
        label = info.pop(label_key, None)
        flatten_info_dict = flatten(info, separator="___")
        node = createNode(label, node_type, flatten_info_dict)
        nodes.append(node)
    return nodes

def createRelationships(first_node, second_node, first_node_attr, second_node_attr, first_node_type, second_node_type, relationship, relationship_attributes_dict):
    relationship_attributes = RelationshipAttributes(relationship_attributes_dict)
    relationship = Relationship(first_node, second_node, first_node_attr, second_node_attr,first_node_type,
                                second_node_type, relationship, relationship_attributes)
    data = relationship.toJSON()
    callServicePost(url=NEO4J_SERVICE_URL + "/relationships/create_relationship", data=data.replace("\n", ""))

openstack_info = {
"SERVERS": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": [
    {"target_attr_name": "OS-EXT-AZ:availability_zone", "target_node_type":"AVAILABILITY_ZONES", "target_node_attr_name":"name" ,"target_value_data_type":"string", "relationship_name":"DEPENDS_ON", "relationship_attrs":{"STATUS":"ACTIVE"}},
    {"target_attr_name": "OS-EXT-SRV-ATTR:host", "target_node_type": "HYPERVISORS", "target_node_attr_name": "service___host", "target_value_data_type": "string", "relationship_name": "RUNS_ON", "relationship_attrs": {"STATUS": "ACTIVE"}}
]
},
"ROUTERS": {
"name_attr":"name",
"data":[],
"RELATIONSHIPS": [
    {"target_attr_name": "external_gateway_info___network_id", "target_node_type":"NETWORKS", "target_node_attr_name":"id" ,"target_value_data_type":"string", "relationship_name":"DEPENDS_ON", "relationship_attrs":{"STATUS":"ACTIVE"}},
    {"target_attr_name": "external_gateway_info___external_fixed_ips___0___subnet_id", "target_node_type":"SUBNETS", "target_node_attr_name":"id" ,"target_value_data_type":"string", "relationship_name":"DEPENDS_ON", "relationship_attrs":{"STATUS":"ACTIVE"}}
]
},
"HOST_AGGREGATES": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": [
	{"target_attr_name": "availability_zone", "target_node_type":"AVAILABILITY_ZONES", "target_node_attr_name":"name" ,"target_value_data_type":"string", "relationship_name":"DEPENDS_ON", "relationship_attrs":{"STATUS":"ACTIVE"}},
	#{"target_attr_name": "hosts___0", "target_node_type":"HYPERVISORS", "target_node_attr_name":"service___host" ,"target_value_data_type":"string", "relationship_name":"CONTAINS", "relationship_attrs":{"STATUS":"ACTIVE"}}
]
},
"AVAILABILITY_ZONES": {
"name_attr":"zoneName",
"data": [],
"RELATIONSHIPS": []
},
"SERVICES": {
"name_attr":"binary",
"data": [],
"RELATIONSHIPS": []
},
"HYPERVISORS": {
"name_attr":"hypervisor_hostname",
"data": [],
"RELATIONSHIPS": []
},
"FLAVORS": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": []
},
"VOLUMES": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": []
},
"KEY_PAIRS": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": []
},
"IMAGES": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": []
},
"NETWORKS": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": [
{"target_attr_name": "subnets___0", "target_node_type":"SUBNETS", "target_node_attr_name":"id" ,"target_value_data_type":"string", "relationship_name":"DEPENDS_ON", "relationship_attrs":{"STATUS":"ACTIVE"}},
{"target_attr_name": "availability_zones___0", "target_node_type":"AVAILABILITY_ZONES", "target_node_attr_name":"name" ,"target_value_data_type":"string", "relationship_name":"DEPENDS_ON", "relationship_attrs":{"STATUS":"ACTIVE"}}
]
},
"SUBNETS": {
"name_attr":"name",
"data": [],
"RELATIONSHIPS": []
}
}

####################################################################################################
def create_servers(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getServers(), key, openstack_info[key]["name_attr"])

def create_host_aggregates(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getHostAggregates(), key, openstack_info[key]["name_attr"])

def create_availability_zones(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getAvailabilityZones(), key, openstack_info[key]["name_attr"])

def create_services(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getServices(), key, openstack_info[key]["name_attr"])

def create_hypervisors(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getHypervisors(), key, openstack_info[key]["name_attr"])

def create_flavors(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getFlavors(), key, openstack_info[key]["name_attr"])

def create_volumes(key):
    openstack_info[key]["data"]=prepareNodesData(cinderQuerier.getVolumes(), key, openstack_info[key]["name_attr"])

def create_key_pairs(key):
    openstack_info[key]["data"]=prepareNodesData(novaQuerier.getKeyPairs(), key, openstack_info[key]["name_attr"])

def create_images(key):
    openstack_info[key]["data"]=prepareNodesData(glanceQuerier.getImages(), key, openstack_info[key]["name_attr"])

def create_networks(key):
    openstack_info[key]["data"]=prepareNodesData(neutronQuerier.getNetworks(), key, openstack_info[key]["name_attr"])

def create_subnets(key):
    openstack_info[key]["data"]=prepareNodesData(neutronQuerier.getSubNets(), key, openstack_info[key]["name_attr"])

def create_routers(key):
    openstack_info[key]["data"]=prepareNodesData(neutronQuerier.getRouters(), key, openstack_info[key]["name_attr"])

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

for key in openstack_info.keys():
    create_graph_elements(key)(key)

for key in openstack_info.keys():
    print("----------------------------------------")
    print(key)
    for d in openstack_info[key]["data"]:
        print(d.__dict__["name"] + ":" + str(d.__dict__["node_attributes"].__dict__))
    # create_graph_elements(key)(key)
####################################################################################################


for key in openstack_info:
    source_node_type = key
    info = openstack_info[key]
    name_attr = openstack_info[key]["name_attr"]
    relationships_info = openstack_info[key]["RELATIONSHIPS"]
    data = openstack_info[key]["data"]
    for relationship in relationships_info:
        target_attr_name = relationship["target_attr_name"]
        target_node_type = relationship["target_node_type"]
        target_node_attr_name = relationship["target_node_attr_name"]
        target_value_data_type = relationship["target_value_data_type"]
        relationship_name = relationship["relationship_name"]
        relationship_attrs = relationship["relationship_attrs"]

        for d in data:
            createRelationships(d.name, d.node_attributes.__dict__[target_attr_name], name_attr, target_node_attr_name, source_node_type, target_node_type, relationship_name, relationship_attrs)
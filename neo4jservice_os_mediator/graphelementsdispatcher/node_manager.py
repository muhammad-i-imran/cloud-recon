from graphserviceschema.serviceschema import *
from httphandler.caller import *


class NodeManager(object):
    NEO4J_SERVICE_URL = ""
    NEO4J_SERVICE_GET_ALL_RELATIVE_PATH = "/nodes/get_all"
    NEO4J_SERVICE_GET_NODE_RELATIVE_PATH = "/nodes/get_node"
    NEO4J_SERVICE_CREATE_NODE_RELATIVE_PATH = "/nodes/create_node"
    NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH = "/nodes/delete_node"
    NEO4J_SERVICE_DELETE_GRAPH_RELATIVE_PATH = "/delete_graph"

    ####################################################################################################################
    """CRUD OPERATIONS"""

    @classmethod
    def create_node(self, id_key, node_type, node_properties_dict):
        node_properties = NodeProperties(node_properties_dict)
        node = Node(id_key=id_key, node_type=node_type, node_properties=node_properties)
        data = node.__dict__
        call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_CREATE_NODE_RELATIVE_PATH,
            data=data)
        return node

    @classmethod
    def update_node(cls, node_type, node_query_properties, node_updated_properties):
        data = {'node_type': node_type, 'node_query_properties': node_query_properties,
                'node_updated_properties': node_updated_properties}
        call_service_put_method(url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH,
                                data=data)

    @classmethod
    def get_node_by_properties(cls, node_properties):
        data = {'node_properties': node_properties}
        # post method because there can be many attributes
        return call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def get_nodes(cls, node_type, node_properties):
        """
        get all nodes by node type and (optionally node properties).
        :param node_type:
        :param node_properties: zero or more elements in a dictionary
        :return:
        """
        data = {'node_type': node_type, 'node_properties': node_properties}
        return call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def get_all_nodes(cls):
        nodes = call_service_get_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_ALL_RELATIVE_PATH)

    @classmethod
    def delete_nodes(cls, node_type, node_properties):
        """
         (leave node_properties empty if you want to delete all nodes of a certain type)
        :param node_type:
        :param node_properties: (dictionary)
        :return:
        """
        data = {'node_type': node_type, 'node_properties': node_properties}
        call_service_delete_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def delete_graph(cls):  ## USE CAREFULLY...
        call_service_delete_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_GRAPH_RELATIVE_PATH)

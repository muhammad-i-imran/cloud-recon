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
    def create_node(self, data: dict):
        """
        Calls web service to create a node.

        :param data: dict
        The data dictionary must contain the following elements:

        id_key: (str) property name that is to be use in graph as a unique attribute
        node_type: (str) the type (for grouping) of the node
        node_properties_dict: (dict) the properties of a node need to be added in graph
        :return:
        """
        call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_CREATE_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def update_node(cls, data: dict):
        """
        Calls web service to update a node.

        :param data: dict
        The data dictionary must contain the following elements:

        node_type: (str) the type of the node
        node_query_properties: (str) the properties of a node needed to query a node to update
        node_updated_properties: (dict) the updated node properties and values
        :return:
        """
        call_service_put_method(url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH,
                                data=data)

    @classmethod
    def get_node_by_properties(cls, data: dict):
        """
        Calls web service to get node(s) by querying by properties.

        :param data: dict
        The data dictionary must contain the following elements:

        node_properties: (str) the properties of a node needed to query a node to update
        :return:
        """

        return call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def get_nodes(cls, data: dict):
        """
        Calls web service to get node(s) by querying by properties.

        :param data: dict
        The data dictionary must contain the following elements:

        node_type: (str) the type of the node
        node_properties: (str) the properties of a node needed to query a node to update
        :return:
        """

        return call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def get_all_nodes(cls):
        """
        Calls web service to get all nodes.

        :return:
        """

        return call_service_get_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_ALL_RELATIVE_PATH)

    @classmethod
    def delete_nodes(cls, data: dict):
        """
        Calls web service to delete a node after querying using the properties.

        :param data: dict
        The data dictionary must contain the following elements:

        node_type: (str) the type of the node
        node_properties: (str) the properties of a node needed to query a node to update
        :return:
        """
        call_service_delete_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH,
            data=data)

    @classmethod
    def delete_graph(cls):
        """
        Deletes the whole graph.

        :return:
        """
        call_service_delete_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_GRAPH_RELATIVE_PATH)

from httphandler.caller import *


from logging_config import Logger

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

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
        logger.info("Calling service to create node.")
        call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_CREATE_NODE_RELATIVE_PATH,
            json=data)

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
        logger.info("Calling service to update node.")
        call_service_put_method(url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH,
                                json=data)

    @classmethod
    def get_node_by_properties(cls, data: dict):
        """
        Calls web service to get node(s) by querying by properties.

        :param data: dict
        The data dictionary must contain the following elements:

        node_type: (str) the type of the node
        node_properties: (str) the properties of a node needed to query a node to update
        :return:
        """
        logger.info("Calling service to get node(s) using query.")
        return call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_NODE_RELATIVE_PATH,
            json=data)

    @classmethod
    def get_nodes(cls, data: dict):
        """
        Calls web service to get node(s) by node type.

        :param data: dict
        The data dictionary must contain the following elements:

        node_type: (str) the type of the node
        :return:
        """
        logger.info("Calling service to get nodes.")
        return call_service_post_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_GET_NODE_RELATIVE_PATH,
            json=data)

    @classmethod
    def get_all_nodes(cls):
        """
        Calls web service to get all nodes.

        :return:
        """
        logger.info("Calling service to get all node.")
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
        logger.info("Calling service to delete node(s).")
        call_service_delete_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_NODE_RELATIVE_PATH,
            json=data)

    @classmethod
    def delete_graph(cls):
        """
        Deletes the whole graph.

        :return:
        """
        logger.info("Calling service to delete the whole graph.")
        call_service_delete_method(
            url=NodeManager.NEO4J_SERVICE_URL + NodeManager.NEO4J_SERVICE_DELETE_GRAPH_RELATIVE_PATH)

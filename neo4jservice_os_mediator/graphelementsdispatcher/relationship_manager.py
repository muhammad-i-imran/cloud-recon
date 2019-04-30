from httphandler.caller import *
from logging_config import Logger

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger


class RelationshipManager(object):
    NEO4J_SERVICE_URL = ""
    NEO4J_SERVICE_CREATE_RELATIONSHIP_RELATIVE_PATH = "/relationships/create_relationship"
    NEO4J_SERVICE_DELETE_RELATIONSHIP_RELATIVE_PATH = "/relationships/delete_relationship"
    NEO4J_SERVICE_DELETE_NODE_ALL_RELATIONSHIPS_RELATIVE_PATH = "/relationships/delete_node_all_relationships"


    @classmethod
    def create_relationship(self, data: dict):
        """
        Calls web service to create a relationship between nodes.

        :param data: dict
        The data dictionary must contain the following elements:

        source_node_type: (str) the source node
        source_node_properties: (dict) the properties that can identify the node in the graph
        target_node_type: (str) the target node
        target_node_properties: (dict) the properties that can identify the node in the graph
        relationship: (str) the useful name of the relationship
        relationship_properties:  (dict) the properties to include in the relationship
        :return:
        """
        logger.info("Calling service to create relationship between nodes.")
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_CREATE_RELATIONSHIP_RELATIVE_PATH,
            json=data)

    @classmethod
    def update_relationship(cls, data: dict):
        logger.info("Calling service to update relationship between nodes.")

        pass

    @classmethod
    def delete_relationship(self, data: dict):
        """
        Calls web service to delete a relationship between nodes.

        :param data: dict
        The data dictionary must contain the following elements:

        source_node_type: (str) the source node
        source_node_properties: (dict) the properties that can identify the node in the graph
        target_node_type: (str) the target node
        target_node_properties: (dict) the properties that can identify the node in the graph
        relationship: (str) the useful name of the relationship
        relationship_properties:  (dict) the properties to include in the relationship
        :return:
        """
        logger.info("Calling service to delete relationship between nodes.")
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_DELETE_RELATIONSHIP_RELATIVE_PATH,
            json=data)

    @classmethod
    def delete_node_all_relationships(self, data: dict):
        """
        Calls web service to delete all relationships of a node.

        :param data: dict
        The data dictionary must contain the following elements:

        node_type: (str) the  node
        node_properties: (dict) the properties that can identify the node in the graph
        :return:
        """
        logger.info("Calling service to delete all relationships of a node.")
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_DELETE_NODE_ALL_RELATIONSHIPS_RELATIVE_PATH,
            json=data)
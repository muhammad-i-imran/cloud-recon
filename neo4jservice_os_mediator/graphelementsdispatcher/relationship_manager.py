from httphandler.caller import *


class RelationshipManager(object):
    NEO4J_SERVICE_URL = ""
    NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH = "/relationships/create_relationship"

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
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH,
            json=data)

    @classmethod
    def update_relationship(cls):
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
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH,
            json=data)

from graphserviceschema.serviceschema import *
from httphandler.caller import *

class RelationshipManager(object):
    NEO4J_SERVICE_URL = ""
    NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH = "/relationships/create_relationship"

    @classmethod
    def create_relationship(self, source_node_type, source_node_properties, target_node_type,
                            target_node_properties, relationship, relationship_properties):
        relationship_properties_obj = RelationshipProperties(relationship_properties)

        relationship = Relationship(source_node_type=source_node_type, source_node_properties=source_node_properties,
                                    target_node_type=target_node_type,
                                    target_node_properties=target_node_properties, relationship=relationship,
                                    relationship_properties=relationship_properties_obj)
        data = relationship.__dict__
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH,
            data=data)

    @classmethod
    def update_relationship(cls):
        pass

    @classmethod
    def delete_relationship(self, source_node_type, source_node_properties, target_node_type,
                                      target_node_properties, relationship, relationship_properties):
        relationship_properties_obj = RelationshipProperties(relationship_properties)

        relationship = Relationship(source_node_type=source_node_type, source_node_properties=source_node_properties,
                                    target_node_type=target_node_type,
                                    target_node_properties=target_node_properties, relationship=relationship,
                                    relationship_properties=relationship_properties_obj)
        data = relationship.__dict__
        call_service_post_method(
            url=RelationshipManager.NEO4J_SERVICE_URL + RelationshipManager.NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH,
            data=data)

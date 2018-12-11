from graphserviceschema.serviceschema import *
from mediator.caller import *

class RelationshipCreator(object):
    NEO4J_SERVICE_URL = ""
    NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH = "/relationships/create_relationship"

    @classmethod
    def createRelationships(self, source_node_attr_name, target_node_attr_name,
                            source_node_attr_value, source_node_type,
                            target_node_type, relationship, relationship_attributes_dict):
        relationship_attributes = RelationshipAttributes(relationship_attributes_dict)

        relationship = Relationship(source_node_attr_name=source_node_attr_name,
                                    target_node_attr_name=target_node_attr_name,
                                    source_node_attr_value=source_node_attr_value,
                                    # target_node_attr_value=target_node_attr_value,
                                    source_node_type=source_node_type,
                                    target_node_type=target_node_type, relationship=relationship,
                                    relationship_attributes=relationship_attributes,
                                    )
        data = relationship.toJSON()
        callServicePost(url=RelationshipCreator.NEO4J_SERVICE_URL + RelationshipCreator.NEO4J_SERVICE_RELATIONSHIP_RELATIVE_PATH, data=data.replace("\n", ""))
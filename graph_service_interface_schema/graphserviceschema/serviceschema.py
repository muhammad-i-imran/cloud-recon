import json
import collections

def depth(dictionary, level=0):
    if not isinstance(dictionary, dict) or not dictionary:
        return level
    return max(depth(dictionary[k], level + 1) for k in dictionary)


class NodeProperties(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, (int, str, bool, float)):
                setattr(self, k, v)

class Node(object):
    def __init__(self, id_key, node_type, node_properties):
        self.id_key = id_key
        # self.name = name
        self.node_type = node_type
        self.node_properties = node_properties

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=0)

class RelationshipProperties(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, (int, str, bool, float)):
                setattr(self, k, v)

class Relationship(object):
    def __init__(self, source_node_type, source_node_properties, target_node_type,
                 target_node_properties, relationship, relationship_properties):
        """

        :param source_node_type:
        :param source_node_properties:
        :param target_node_type:
        :param target_node_properties:
        :param relationship:
        :param relationship_properties:
        """
        self.source_node_type = source_node_type
        self.source_node_properties = source_node_properties

        self.target_node_type = target_node_type
        self.target_node_properties = target_node_properties

        self.relationship = relationship
        self.relationship_properties = relationship_properties

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=0)
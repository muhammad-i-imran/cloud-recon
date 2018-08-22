import json
import collections

def depth(dictionary, level=0):
    if not isinstance(dictionary, dict) or not dictionary:
        return level
    return max(depth(dictionary[k], level + 1) for k in dictionary)

class NodeAttributes(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, (int, str, bool, float)):
                setattr(self, k, v)
class Node(object):
    def __init__(self, label, node_type, node_attributes):
        self.label = label
        self.node_type = node_type
        self.node_attributes = node_attributes

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=0)

class RelationshipAttributes(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, (int, str, bool, float)):
                setattr(self, k, v)

class Relationship(object):
    def __init__(self, first_node, second_node, first_node_attr, second_node_attr, first_node_type, second_node_type, relationship, relationship_attributes):
        self.first_node = first_node
        self.second_node = second_node

        self.first_node_attr=first_node_attr
        self.second_node_attr=second_node_attr

        self.first_node_type = first_node_type
        self.second_node_type = second_node_type

        self.relationship = relationship
        self.relationship_attributes = relationship_attributes

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=0)

#TODO: CHECK WHETHER WE NEED TO CREATE ANOTHER CLASS FOR UPDATING NODE OR RELATIONSHIPS OR THEIR ATTRIBUTES

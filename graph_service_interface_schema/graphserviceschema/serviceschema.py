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
    def __init__(self, id_key, node_type, node_attributes):
        self.id_key = id_key
        # self.name = name
        self.node_type = node_type
        self.node_attributes = node_attributes

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=0)


class RelationshipAttributes(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, (int, str, bool, float)):
                setattr(self, k, v)


# TODO: REFACTOR IT LATER
class Relationship(object):
    def __init__(self, source_node_attr_name, target_node_attr_name, source_node_attr_value,
                 source_node_type,
                 target_node_type, relationship, relationship_attributes, is_source_attr_name_regex):
        self.source_node_attr_name = source_node_attr_name
        self.target_node_attr_name = target_node_attr_name

        self.source_node_attr_value = source_node_attr_value
        # self.target_node_attr_value = target_node_attr_value

        self.source_node_type = source_node_type
        self.target_node_type = target_node_type

        self.relationship = relationship
        self.relationship_attributes = relationship_attributes

        self.is_source_attr_name_regex = is_source_attr_name_regex
        # self.is_target_attr_name_regex = is_target_attr_name_regex

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=0)

# TODO: CHECK WHETHER WE NEED TO CREATE ANOTHER CLASS FOR UPDATING NODE OR RELATIONSHIPS OR THEIR ATTRIBUTES

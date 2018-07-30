import json

def depth(dictionary, level=0):
    if not isinstance(dictionary, dict) or not dictionary:
        return level
    return max(depth(dictionary[k], level + 1) for k in dictionary)

class NodeAttributes(object):
    def _get_node_name(self):
        return self.__node_name

    def _set_node_name(self, value):
        if not isinstance(value, str):
            raise TypeError("node_name must be a string.")
        # if depth(value) > 1:
        #     raise ValueError("The dictionary depth must be 1")
        self.__node_name = value

    node_name = property(_get_node_name, _set_node_name)
    #TODO: LIST OTEHR ATTRIBUTES THAT WE WILL NEED

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

class Node(object):
    def _get_label(self):
        return self.__label

    def _set_label(self, value):
        if not isinstance(value, str):
            raise TypeError("label must be a string.")
        self.__label = value

    def _get_node_type(self):
        return self.__node_type

    def _set_node_type(self, value):
        if not isinstance(value, str):
            raise TypeError("node_type must be a string.")
        self.__node_type = value

    def _get_node_attributes(self):
        return self.__node_attributes

    def _set_node_attributes(self, value):
        if not isinstance(value, NodeAttributes):
            raise TypeError("node_attributes must be an object of Node Attributes")
        self.__node_attributes = value

    label = property(_get_label, _set_label)
    node_type = property(_get_node_type, _set_node_type)
    node_attributes = property(_get_node_attributes, _set_node_attributes)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

class RelationshipAttributes(object):
    def _get_relationship_name(self):
        return self.__relationship_name

    def _set_relationship_name(self, value):
        if not isinstance(value, str):
            raise TypeError("relationship_name must be a string.")
        # if depth(value) > 1:
        #     raise ValueError("The dictionary depth must be 1")
        self.__relationship_name = value

    relationship_name = property(_get_relationship_name, _set_relationship_name)
    #TODO: LIST OTEHR ATTRIBUTES THAT WE WILL NEED

    #
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

class Relationship(object):

    def _get_first_node(self):
        return self.__first_node

    def _set_first_node(self, value):
        if not isinstance(value, str):
            raise TypeError("first_node must be a string.")
        self.__first_node = value

    def _get_second_node(self):
        return self.__second_node

    def _set_second_node(self, value):
        if not isinstance(value, str):
            raise TypeError("second_node must be a string.")
        self.__second_node = value

    def _get_first_node_type(self):
        return self.__first_node_type

    def _set_first_node_type(self, value):
        if not isinstance(value, str):
            raise TypeError("first_node_type must be a string.")
        self.__first_node_type = value


    def _get_second_node_type(self):
        return self.__second_node_type

    def _set_second_node_type(self, value):
        if not isinstance(value, str):
            raise TypeError("first_node_type must be a string.")
        self.__second_node_type = value

    def _get_relationship(self):
        return self.__relationship

    def _set_relationship(self, value):
        if not isinstance(value, str):
            raise TypeError("relationship must be an object of string.")
        self.__relationship = value

    def _get_relationship_attributes(self):
        return self.__relationship_attributes

    def _set_relationship_attributes(self, value):
        if not isinstance(value, RelationshipAttributes):
            raise TypeError("relationship_attributes must be an object of RelationshipAttributes.")
        self.__relationship_attributes = value

    first_node = property(_get_first_node, _set_first_node)
    second_node = property(_get_second_node, _set_second_node)
    first_node_type = property(_get_first_node_type, _set_first_node_type)
    second_node_type = property(_get_second_node_type, _set_second_node_type)
    relationship = property(_get_relationship, _set_relationship)
    relationship_attributes = property(_get_relationship_attributes, _set_relationship_attributes)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

#TODO: CHECK WHETHER WE NEED TO CREATE ANOTHER CLASS FOR UPDATING NODE OR RELATIONSHIPS OR THEIR ATTRIBUTES
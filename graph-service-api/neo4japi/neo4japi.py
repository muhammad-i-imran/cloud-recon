from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

from neo4japi import IllegalArgumentError


class Neo4JApi(object):
    def __init__(self, uri, user, password):
        self.graph = Graph(uri=uri, user=user, password=password)

    def get_nodes(self, node_type):
        matcher = NodeMatcher(self.graph)
        nodes = matcher.match(node_type) #.match(first_node_type, name=first_node).first()
        return list(nodes)

    def create_node(self, node_type, label, node_attributes={}):
        if not label:
            raise IllegalArgumentError('You must have to provide a label.')
        if not node_attributes:
            node_attributes={}
        # nesting is not allowed by the API
        dict_depth = self.__depth(node_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        node = Node(node_type, name=label, **node_attributes)
        self.graph.create(node)

    def create_relationship(self, first_node_type, second_node_type,first_node, second_node, relationship, relationship_attributes):
        if not first_node or not  second_node or not relationship:
            raise IllegalArgumentError("Please provide valid nodes and relationships.")
        dict_depth = self.__depth(relationship_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        #TODO: check if we can add relationships to all nodes with same names and types (instead of taking first())
        matcher = NodeMatcher(self.graph)
        node1=matcher.match(first_node_type, name=first_node)#.first()
        node2 = matcher.match(second_node_type, name=second_node)#.first()

        self.graph.create(Relationship(node1, relationship, node2, **relationship_attributes))

    def add_node_attr(self, node_type, node_name, node_attributes):
        matcher = NodeMatcher(self.graph)
        #TODO: try not to use first() here
        node = matcher.match(node_type, name=node_name).first()
        # node = Node(node_type, name=node_name, )
        # self.graph.merge(node)
        node.update(**node_attributes)
        self.graph.push(node)

    def add_relationship_attr(self, first_node_type, second_node_type, first_node_name, second_node_name, relationship, relationship_attributes):
        if not relationship:
            raise IllegalArgumentError("Relationship is not specified.")
        dict_depth = self.__depth(relationship_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")
        matcher = NodeMatcher(self.graph)
        node1 = matcher.match(first_node_type, name=first_node_name).first()
        node2 = matcher.match(second_node_type, name=second_node_name).first()
        for rel in self.graph.match((node1,node2), relationship):
            rel.update(**relationship_attributes)
            self.graph.push(rel)

    #TODO: check whether relationships are still there after deleting nodes or relationships are also deleted
    def delete_node(self, node_type, node_name):
        matcher = NodeMatcher(self.graph)
        #TODO: try not to use first() here. to check whether it remoces multiple nodes if we remove first()
        node = matcher.match(node_type, name=node_name).first()
        self.graph.delete(node)

    #TODO: check whether relationships are still there after deleting nodes or relationships are also deleted
    def delete_multiple_nodes(self, list_node_type_name_mapping):
        for node in list_node_type_name_mapping:
            self.delete_node(node["node_type"], node["node_name"])

    def delete_relationship_between_nodes(self, first_node_type, first_node_name, second_node_type, second_node_name, relationship, relationship_attributes):
        dict_depth = self.__depth(relationship_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        matcher = NodeMatcher(self.graph)
        # find nodes
        node1 = matcher.match(first_node_type, name=first_node_name).first()
        node2 = matcher.match(second_node_type, name=second_node_name).first()

        rel_matcher = RelationshipMatcher(self.graph)
        # find the given relationship between the given nodes
        relationship_to_del = rel_matcher.match(node1, node2, r_type=relationship, properties=relationship_attributes)

        # remove the relationship
        self.graph.delete(relationship_to_del)

    def delete_multiple_relationships(self, list_of_relationship_dict):
        #format: array of dict: [{first_node_type, first_node_name, second_node_type, second_node_name, relationship, relationship_attributes}]
        for relationship_info in list_of_relationship_dict:
            self.delete_relationship_between_nodes(relationship_info["first_node_type"], relationship_info["first_node_name"], relationship_info["second_node_type"], relationship_info["second_node_name"], relationship_info["relationship"], relationship_info["relationship_attributes"])

    def create_multiple_nodes(self, list_node_info):
        # [{node_type, label, node_attributes}]
        for node in list_node_info:
            self.create_node(node["node_type"], node["label"], node["node_attributes"])

    def create_multiple_relationships(self, list_relationship_info):
        # [{first_node_type, second_node_type,first_node_name, second_node_name, relationship, relationship_attributes}]
        for node in list_relationship_info:
            self.create_relationship(node["first_node_type"], node["second_node_type"], node["first_node_name"], node["second_node_name"], node["relationship"], node["relationship_attributes"])

    def delete_all(self):
        self.graph.delete_all()


    #def close(self):
    #    return

    def __depth(self, dictionary, level=0):
        if not isinstance(dictionary, dict) or not dictionary:
            return level
        return max(self.__depth(dictionary[k], level + 1) for k in dictionary)
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

import IllegalArgumentError


class Neo4JApi(object):
    def __init__(self, uri, user, password):
        self.graph = Graph(uri=uri, user=user, password=password)
        # self.graph.schema.create_uniqueness_constraint('type', 'id')


    def get_nodes(self, node_type):
        matcher = NodeMatcher(self.graph)
        nodes = matcher.match(node_type)  # .match(first_node_type, name=first_node).first()
        return list(nodes)

    def create_node(self, node_type, id_keys, label, node_attributes={}):
        # TODO: create only unique nodes. move ti somewhere else later to avoid repetition of execution of this line
        self.graph.schema.create_uniqueness_constraint(node_type, *id_keys)

        if not label:
            raise IllegalArgumentError('You must have to provide a label.')
        if not node_attributes:
            node_attributes = {}
        # nesting is not allowed by the API
        dict_depth = self.__depth(node_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        node = Node(node_type, name=label, **node_attributes)
        try:
            self.graph.create(node)
            return 201, "Node has been created."
        except Exception as ex:
            print("Exception occured: ", ex)
            return 304, str(ex)

    def find_node(self, element_type, attribute_name, attribute_value):
        matcher = NodeMatcher(self.graph)
        nodes = matcher.match(element_type).where(
            "_." + attribute_name + "='" + attribute_value + "'")  # .first() #.order_by("_.name").limit(3)
        return nodes

    def find_node_with_regex(self, element_type, attribute_name, attribute_value_regex):
        matcher = NodeMatcher(self.graph)
        nodes = matcher.match(element_type).where(
            "_." + attribute_name + "=~'" + attribute_value_regex + "'")  # .first() #.order_by("_.name").limit(3)
        return nodes

    ###############################################
    ### REFACTOR create_relationship() and add is_***_regex attributes as well
    def create_relationship(self, source_node_type, target_node_type,
                            source_node_attr_value,
                            target_node_attr_value, source_node_attr_name,
                            target_node_attr_name, relationship,
                            relationship_attributes, is_source_attr_name_regex=False,
                            is_target_attr_name_regex=False):
        if not relationship:
            raise IllegalArgumentError("Please provide valid relationships.")

        dict_depth = self.__depth(relationship_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        # TODO: check if we can add relationships to all nodes with same names and types (instead of taking first())

        if is_source_attr_name_regex:
            source_nodes = self.find_node_with_regex(source_node_type, source_node_attr_name, source_node_attr_value)
        else:
            source_nodes = self.find_node(source_node_type, source_node_attr_name, source_node_attr_value)

        if is_target_attr_name_regex:
            target_nodes = self.find_node_with_regex(target_node_type, target_node_attr_name, target_node_attr_value)
        else:
            target_nodes = self.find_node(target_node_type, target_node_attr_name, target_node_attr_value)

        for node1 in source_nodes:
            for node2 in target_nodes:
                self.graph.create(Relationship(node1, relationship, node2, **relationship_attributes))

    ###############################################

    # def create_relationship(self, first_node_type, second_node_type, first_node, second_node, first_node_attr,
    #                         second_node_attr, relationship, relationship_attributes):
    #     if not first_node or not second_node or not relationship:
    #         raise IllegalArgumentError("Please provide valid nodes and relationships.")
    #     dict_depth = self.__depth(relationship_attributes)
    #     if dict_depth > 1:
    #         raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")
    #
    #     # TODO: check if we can add relationships to all nodes with same names and types (instead of taking first())
    #
    #     nodes_1 = self.find_node(first_node_type, first_node_attr, first_node)
    #     nodes_2 = self.find_node(second_node_type, second_node_attr, second_node)
    #
    #     for node1 in nodes_1:
    #         for node2 in nodes_2:
    #             self.graph.create(Relationship(node1, relationship, node2, **relationship_attributes))
    #
    #################################################

    def add_node_attr(self, node_type, node_name, node_attributes):
        matcher = NodeMatcher(self.graph)
        # TODO: try not to use first() here
        node = matcher.match(node_type, name=node_name).first()
        # node = Node(node_type, name=node_name, )
        # self.graph.merge(node)
        node.update(**node_attributes)
        self.graph.push(node)

    def add_relationship_attr(self, first_node_type, second_node_type, first_node_name, second_node_name, relationship,
                              relationship_attributes):
        if not relationship:
            raise IllegalArgumentError("Relationship is not specified.")
        dict_depth = self.__depth(relationship_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")
        matcher = NodeMatcher(self.graph)
        node1 = matcher.match(first_node_type, name=first_node_name).first()
        node2 = matcher.match(second_node_type, name=second_node_name).first()
        for rel in self.graph.match((node1, node2), relationship):
            rel.update(**relationship_attributes)
            self.graph.push(rel)

    # TODO: check whether relationships are still there after deleting nodes or relationships are also deleted
    def delete_node(self, node_type, node_name):
        matcher = NodeMatcher(self.graph)
        # TODO: try not to use first() here. to check whether it remoces multiple nodes if we remove first()
        node = matcher.match(node_type, name=node_name).first()
        self.graph.delete(node)

    # TODO: check whether relationships are still there after deleting nodes or relationships are also deleted
    def delete_multiple_nodes(self, list_node_type_name_mapping):
        for node in list_node_type_name_mapping:
            self.delete_node(node["node_type"], node["node_name"])

    def delete_relationship_between_nodes(self, first_node_type, first_node_name, second_node_type, second_node_name,
                                          relationship, relationship_attributes):
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
        # format: array of dict: [{first_node_type, first_node_name, second_node_type, second_node_name, relationship, relationship_attributes}]
        for relationship_info in list_of_relationship_dict:
            self.delete_relationship_between_nodes(relationship_info["first_node_type"],
                                                   relationship_info["first_node_name"],
                                                   relationship_info["second_node_type"],
                                                   relationship_info["second_node_name"],
                                                   relationship_info["relationship"],
                                                   relationship_info["relationship_attributes"])

    def create_multiple_nodes(self, list_node_info):
        # [{node_type, label, node_attributes}]
        for node in list_node_info:
            self.create_node(node["node_type"], node["label"], node["node_attributes"])

    def create_multiple_relationships(self, list_relationship_info):
        # [{first_node_type, second_node_type,first_node_name, second_node_name, relationship, relationship_attributes}]
        for node in list_relationship_info:
            self.create_relationship(node["first_node_type"], node["second_node_type"], node["first_node_name"],
                                     node["second_node_name"], node["relationship"], node["relationship_attributes"])

    def delete_all(self):
        self.graph.delete_all()

    def __depth(self, dictionary, level=0):
        if not isinstance(dictionary, dict) or not dictionary:
            return level
        return max(self.__depth(dictionary[k], level + 1) for k in dictionary)

    def __del__(self):
        print("Close connection here.")
        # del self.graph

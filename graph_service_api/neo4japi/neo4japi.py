from py2neo import *
from .IllegalArgumentError import IllegalArgumentError

class Neo4JApi(object):

    def __init__(self, uri=None, host='localhost', port=7687, user='neo4j', password=None, scheme='bolt', secure=False):
        """

        :param uri:
        :param host:
        :param port:
        :param user:
        :param password:
        :param scheme:
        :param secure:
        """
        self.graph = Graph(uri=uri, host=host, port=port, user=user, password=password, scheme=scheme,
                           secure=secure)

    """ 'OVERLOADED' CONSTRUCTORS """

    @classmethod
    def init(cls, uri, user, password):
        """

        :param uri:
        :param user:
        :param password:
        :return:
        """
        return cls(uri=uri, user=user, password=password)

    @classmethod
    def init_with_settings(cls, uri=None, host='localhost', port=7687, user='neo4j', password=None, scheme='bolt',
                           secure=False):
        """

        :param uri:
        :param host:
        :param port:
        :param user:
        :param password:
        :param scheme:
        :param secure:
        :return:
        """
        return cls(uri=uri, host=host, port=port, user=user, password=password, scheme=scheme, secure=secure)

    ####################################################################################################################

    def get_node_types(self):
        """ Get all node types available in the graph

        :param  :
        """
        return set(self.graph.schema.node_types)

    def get_relationship_types(self):
        """ Get all relationship types available in the graph

        :param  :
        """
        return set(self.graph.schema.relationship_types)

    def get_all_nodes(self):  # TODO: check returned data format
        """
        Return all nodes
        :return:
        """
        query = "MATCH (n) RETURN n"
        results = self.graph.run(cypher=query).data()
        return results

    def get_all_nodes_by_type(self, node_type):  ##e.g. MATCH (n: VOLUMES) RETURN n
        """

        :param node_type:
        :return:
        """
        matcher = NodeMatcher(self.graph)
        nodes = matcher.match(node_type)
        return list(nodes)

    def create_node(self, node_type, primary_keys, node_attributes):
        """

        :param node_type:
        :param primary_keys:
        :param node_attributes: should also contain attribute 'name'
        :return:
        """
        if primary_keys is not None:
            try:
                self.graph.schema.create_uniqueness_constraint(node_type, *primary_keys)
            except Exception as ex:
                pass

        dict_depth = self.__depth(node_attributes)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")
        node = Node(node_type, **node_attributes)
        try:
            self.graph.create(node)
            return str(node), 200
        except Exception as ex:
            return str(ex), 304

    def create_node_with_merge(self, node_type, primary_keys, node_attributes):
        """
        Creates node if it doesn't exist, otherwise merge it. Good for updation

        :param node_type:
        :param id_key:
        :param node_attributes:
        :return:
        """
        node = Node(node_type, **node_attributes)
        try:
            self.graph.merge(node, node_type, *primary_keys)
            return str(node), 200
        except Exception as ex:
            return str(ex), 304

    ###############################################
    # def create_relationship(self, source_node_type, target_node_type,
    #                         source_node_attr_value,
    #                         target_node_attr_value, source_node_attr_name,
    #                         target_node_attr_name, relationship,
    #                         relationship_attributes, is_source_attr_name_regex=False,
    #                         is_target_attr_name_regex=False):
    def create_relationship(self, source_node_type, source_node_attributes, target_node_type,
                            target_node_attributes, relationship,
                            relationship_attributes):
        pass

        # if not relationship:
        #     raise IllegalArgumentError("Please provide valid relationships.")
        #
        # dict_depth = self.__depth(relationship_attributes)
        # if dict_depth > 1:
        #     raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")
        #
        #
        # if is_source_attr_name_regex:
        #     source_nodes = self.find_node_with_regex(source_node_type, source_node_attr_name, source_node_attr_value)
        # else:
        #     source_nodes = self.find_node(source_node_type, source_node_attr_name, source_node_attr_value)
        #
        # if is_target_attr_name_regex:
        #     target_nodes = self.find_node_with_regex(target_node_type, target_node_attr_name, target_node_attr_value)
        # else:
        #     target_nodes = self.find_node(target_node_type, target_node_attr_name, target_node_attr_value)
        #
        # for node1 in source_nodes:
        #     for node2 in target_nodes:
        #         self.graph.create(Relationship(node1, relationship, node2, **relationship_attributes))

    def add_node_attr(self, node_type, node_name, node_attributes):
        matcher = NodeMatcher(self.graph)
        # TODO: try not to use first() here
        node = matcher.match(node_type, name=node_name).first()
        # node = Node(node_type, name=node_name, )
        # self.graph.merge(node)
        node.update(**node_attributes)
        self.graph.push(node)

    def add_relationship_attr(self, source_node_type, source_node_attributes, target_node_type, target_node_attributes,
                              relationship, new_relationship_attributes):
        """

        :param source_node_type:
        :param source_node_attributes:
        :param target_node_type:
        :param target_node_attributes:
        :param relationship:
        :param new_relationship_attributes:
        :return:
        """

    # if not relationship:
    #     raise IllegalArgumentError("Relationship is not specified.")
    # dict_depth = self.__depth(relationship_attributes)
    # if dict_depth > 1:
    #     raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")
    # matcher = NodeMatcher(self.graph)
    # node1 = matcher.match(first_node_type, name=first_node_name).first()
    # node2 = matcher.match(second_node_type, name=second_node_name).first()
    # for rel in self.graph.match((node1, node2), relationship):
    #     rel.update(**relationship_attributes)
    #     self.graph.push(rel)

    # TODO: check whether relationships are still there after deleting nodes or relationships are also deleted
    def delete_nodes(self, node_type, properties_dict):
        """

        :param node_type:
        :param properties_dict:
        :return:
        """
        nodes = self.find_nodes(node_type, properties_dict)
        for node in nodes:
            self.graph.delete(node)
        return 200

    def remove_relationship(self, source_node_type, source_node_properties_dict, target_node_type,
                            target_node_properties_dict, relationship_type, relationship_attributes):
        """

        :param source_node_type:
        :param source_node_properties_dict:
        :param target_node_type:
        :param target_node_properties_dict:
        :param relationship_type:
        :param relationship_attributes:
        :return:

        """
        # matcher = NodeMatcher(self.graph)
        # # find nodes
        # node1 = matcher.match(first_node_type, name=first_node_name).first()
        # node2 = matcher.match(second_node_type, name=second_node_name).first()
        #
        # rel_matcher = RelationshipMatcher(self.graph)
        # # find the given relationship between the given nodes
        # relationship_to_del = rel_matcher.match(node1, node2, r_type=relationship, properties=relationship_attributes)
        #
        # # remove the relationship
        # self.graph.delete(relationship_to_del)

        source_nodes = self.find_nodes(source_node_type, source_node_properties_dict)
        target_nodes = self.find_nodes(target_node_type, target_node_properties_dict)
        relationships = self.find_relationships(source_nodes, target_nodes, relationship_type, relationship_attributes)
        for relationship in relationships:
            self.graph.delete(relationship)

    ####################################################################################################################
    def find_relationships(self, source_node, target_node, relationship_type, relationship_attributes):
        """

        :param source_node:
        :param target_node:
        :param relationship_type:
        :param relationship_attributes:
        :return:
        """
        relationship_matcher = RelationshipMatcher(self.graph)
        relationships = relationship_matcher.match(source_node, target_node, r_type=relationship_type,
                                                   properties=relationship_attributes)
        return relationships

    def find_nodes(self, node_type, properties_dict):
        """

        :param node_type:
        :param properties_dict:
        :return:
        """
        matcher = NodeMatcher(self.graph)
        nodes = matcher.match(node_type, **properties_dict)
        return nodes, 200

    def find_node_with_regex(self, node_type, properties_dict):
        """

        :param node_type:
        :param properties_dict:
        :return: nodes that matched the crieteria and status code
        """
        matcher = NodeMatcher(self.graph)
        where_clauses = []
        for key, value in properties_dict:
            where_clauses.append("_." + key + "=~'" + value + "'")
        nodes = matcher.match(node_type).where(*where_clauses)
        return nodes, 200

    def does_node_exist(self, node_type, properties_dict):
        pass

    ####################################################################################################################

    def delete_all(self):
        """
        Deletes all nodes and relationships
        :return: Status code
        """
        try:
            self.graph.delete_all()
            return 200
        except Exception as e:
            return 304

    ####################################################################################################################

    """ Helper method """

    def __depth(self, dictionary, level=0):
        if not isinstance(dictionary, dict) or not dictionary:
            return level
        return max(self.__depth(dictionary[k], level + 1) for k in dictionary)

    def __del__(self):
        try:
            pass
            # self.graph.close()
        finally:
            del self.graph

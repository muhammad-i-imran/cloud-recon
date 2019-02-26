from py2neo import *
# from .IllegalArgumentError import IllegalArgumentError

class Neo4JApi(object):

    def __init__(self, host='localhost', port=7687, user='neo4j', password=None, scheme='bolt', secure=False):
        """

        :param uri:
        :param host:
        :param port:
        :param user:
        :param password:
        :param scheme:
        :param secure:
        """
        self.graph = Graph(host=host, port=port, user=user, password=password, scheme=scheme,
                           secure=secure)

    """ 'OVERLOADED' CONSTRUCTORS """

    # @classmethod
    # def init(cls, uri, user, password):
    #     """
    #
    #     :param uri:
    #     :param user:
    #     :param password:
    #     :return:
    #     """
    #     return cls(uri=uri, user=user, password=password)

    @classmethod
    def init_with_settings(cls, host='localhost', port=7687, user='neo4j', password=None, scheme='bolt',
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
        return cls(host=host, port=port, user=user, password=password, scheme=scheme, secure=secure)

    ####################################################################################################################

    def get_node_types(self):
        """ Get all node types available in the graph

        :param  :
        """
        return set(self.graph.schema.node_labels)

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

    # def get_all_nodes_by_type(self, node_type):  ##e.g. MATCH (n: VOLUMES) RETURN n
    #     """
    #
    #     :param node_type:
    #     :return:
    #     """
    #     matcher = NodeMatcher(self.graph)
    #     nodes = matcher.match(node_type)
    #     return list(nodes)

    def get_nodes(self, node_type, node_properties):
        """

        :param node_type:
        :param node_properties:
        :return:
        """
        nodes, status = self.find_nodes(node_type=node_type, properties_dict=node_properties)
        return  list(nodes), status


    def create_node(self, node_type, primary_keys, node_properties):
        """

        :param node_type:
        :param primary_keys:
        :param node_properties: should also contain attribute 'name'
        :return:
        """
        if primary_keys is not None:
            try:
                self.graph.schema.create_uniqueness_constraint(node_type, *primary_keys)
            except Exception as ex:
                pass

        dict_depth = self.__depth(node_properties)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. properties JSON should have depth 1.")
        node = Node(node_type, **node_properties)
        try:
            self.graph.create(node)
            return 200
        except Exception as ex:
            return 304

    def create_node_with_merge(self, node_type, primary_keys, node_properties):
        """
        Creates node if it doesn't exist, otherwise merge it. Good for updation

        :param node_type:
        :param id_key:
        :param node_properties:
        :return:
        """
        node = Node(node_type, **node_properties)
        try:
            self.graph.merge(node, node_type, *primary_keys)
            return 200
        except Exception as ex:
            return 304

    def create_relationship(self, source_node_type, source_node_properties, target_node_type,
                            target_node_properties, relationship,
                            relationship_properties):
        """

        :param source_node_type:
        :param source_node_properties:
        :param target_node_type:
        :param target_node_properties:
        :param relationship:
        :param relationship_properties:
        :return:
        """

        dict_depth = self.__depth(relationship_properties)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. properties JSON should have depth 1.")

        # todo: check if properties names/values are regexes

        source_nodes = self.find_nodes(source_node_type, source_node_properties)
        target_nodes = self.find_nodes(target_node_type, target_node_properties)

        if source_nodes and target_nodes:
            for source_node in source_nodes:
                for target_node in target_nodes:
                    self.graph.create(Relationship(source_node, relationship, target_node, **relationship_properties))
        return 200

    def create_relationship_with_merge(self, source_node_type, source_node_properties, target_node_type,
                            target_node_properties, relationship,
                            relationship_properties):
        """
        [this is recommended if you don't want to create duplicates.]

        :param source_node_type:
        :param source_node_properties:
        :param target_node_type:
        :param target_node_properties:
        :param relationship:
        :param relationship_properties:
        :return:
        """

        dict_depth = self.__depth(relationship_properties)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. properties JSON should have depth 1.")

        # todo: check if properties names/values are regexes

        source_nodes = self.find_nodes(source_node_type, source_node_properties)
        target_nodes = self.find_nodes(target_node_type, target_node_properties)

        if source_nodes and target_nodes:
            for source_node in source_nodes:
                for target_node in target_nodes:
                    self.graph.merge(Relationship(source_node, relationship, target_node, **relationship_properties))
        return 200

    def update_node_properties(self, node_type, node_query_properties, node_updated_properties):
        """

        :param node_type:
        :param node_query_properties:
        :param node_updated_properties:
        :return:
        """
        nodes = self.find_nodes(node_type, node_query_properties)
        for node in nodes:
            node.update(**node_updated_properties)
            self.graph.push(node)
        return 200

    def delete_node(self, node_type, properties_dict):
        """

        :param node_type:
        :param properties_dict:
        :return:
        """
        nodes = self.find_nodes(node_type, properties_dict)
        for node in nodes:
            self.graph.delete(node)
        return 200

    def delete_relationship(self, source_node_type, source_node_properties_dict, target_node_type,
                            target_node_properties_dict, relationship_type, relationship_properties):
        """

        :param source_node_type:
        :param source_node_properties_dict:
        :param target_node_type:
        :param target_node_properties_dict:
        :param relationship_type:
        :param relationship_properties:
        :return:
        """
        source_nodes = self.find_nodes(source_node_type, source_node_properties_dict)
        target_nodes = self.find_nodes(target_node_type, target_node_properties_dict)
        relationships = self.find_relationships(source_nodes, target_nodes, relationship_type, relationship_properties)
        for relationship in relationships:
            self.graph.separate(relationship)
        return 200

    ####################################################################################################################
    def find_relationships(self, source_node, target_node, relationship_type, relationship_properties):
        """

        :param source_node:
        :param target_node:
        :param relationship_type:
        :param relationship_properties:
        :return:
        """
        relationship_matcher = RelationshipMatcher(self.graph)
        relationships = relationship_matcher.match(source_node, target_node, r_type=relationship_type,
                                                   properties=relationship_properties)
        return relationships, 200

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

    # def __del__(self):
    #     try:
    #         pass
    #         # self.graph.close()
    #     finally:
    #         del self.graph


# import json
# g=Neo4JApi.init_with_settings(host='10.0.42.181', port=7474, user='neo4j', password=None, scheme='http', secure=False)
# nodes,status=g.get_nodes("VOLUMES", {})
# for node in nodes:
#     print(json.dumps(node))
from neo4j.v1 import GraphDatabase, Session, ServiceUnavailable, custom_auth, TRUST_ALL_CERTIFICATES
import json
from .IllegalArgumentError import IllegalArgumentError


class Neo4JApi(object):
    def __init__(self, uri, **parameters):
        self._driver = GraphDatabase.driver(uri=uri, **parameters)

    """ 'OVERLOADED' CONSTRUCTORS """

    ### TODO: Connection pool management
    @classmethod
    def init_with_basic_auth(cls, uri, user, password, encrypted=True, connection_timeout=30, max_retry_time=10,
                             trust=TRUST_ALL_CERTIFICATES):
        return cls(uri, auth=(user, password), encrypted=encrypted, connection_timeout=connection_timeout,
                   max_retry_time=max_retry_time, trust=trust)

    @classmethod
    def init_with_kerberos_auth(cls, uri, ticket, encrypted=True, connection_timeout=30, max_retry_time=10,
                                trust=TRUST_ALL_CERTIFICATES):
        return cls(uri, auth=(ticket), encrypted=encrypted, connection_timeout=connection_timeout,
                   max_retry_time=max_retry_time, trust=trust)

    @classmethod
    def init_with_custom_auth(cls, uri, principal, credentials, realm, scheme, encrypted=True, connection_timeout=30,
                              max_retry_time=10, trust=TRUST_ALL_CERTIFICATES, **parameters):
        return cls(uri, auth=custom_auth(principal, credentials, realm, scheme, **parameters), encrypted=encrypted,
                   connection_timeout=connection_timeout,
                   max_retry_time=max_retry_time, trust=trust)

    """CRUD Operations"""
    """All transactions are auto-commit"""

    def get_all_node(self):
        query = "MATCH (n) RETURN n"
        result = TransactionExecutor.execute_query_read_transaction_function(self._driver, query)
        return result

    def create_node(self, node_type, id_key, node_attributes={}):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
        print(node_type + ":" + id_key + ">>>>>" + str(node_attributes))
        node_attributes_string = ", ".join(
            ["=".join(["n." + "`{0}`".format(key), "'{0}'".format(val)]) for key, val in node_attributes.items()])
        query = "MERGE (n: {0}{{ {1}: '{2}' }}) ON CREATE SET {3} ON MATCH SET {4} RETURN n"
        query = query.format(node_type, id_key, node_attributes.get(id_key, None), node_attributes_string,
                             node_attributes_string)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def create_relationship(self, source_node_type, target_node_type,
                            source_node_attr_value,
                            target_node_attr_value, source_node_attr_name,
                            target_node_attr_name, relationship,
                            relationship_attributes):

        if not relationship:
            raise IllegalArgumentError("Please provide valid relationships.")

        dict_depth = self.__depth(dictionary=relationship_attributes, level=0)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        # source_regex_operator = "" if is_source_attr_name_regex else ""
        # target_regex_operator = "~" if is_target_attr_name_regex else ""

        value = "'" + source_node_attr_value + "'" if type(source_node_attr_value) is str else source_node_attr_value

        query = "MATCH(m: {0}) WHERE m.`{1}`={2} MATCH(n:{3}) WHERE n.`{4}`={5} MERGE(m)-[r:{6}]->(n) RETURN r"
        query = query.format(source_node_type, source_node_attr_name, value,
                             target_node_type,
                             target_node_attr_name, value, relationship)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def replace_node_attr(self, node_type, node_name_attr, node_name, node_attributes):
        query = "MATCH (n: {0}) WHERE n.{1}={2} SET n={3} RETURN n"
        query = query.format(node_type, node_name_attr, node_name, node_attributes)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def remove_node_all_attr(self, node_type, node_name_attr, node_name):
        query = "MATCH (n: {0}) WHERE n.{1}={2} SET n = {{}} RETURN n"
        query = query.format(node_type, node_name_attr, node_name)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def remove_node_attr(self, node_type, query_attribute, query_attribute_value, attribute_to_remove):
        query = "MATCH (n: {0}) WHERE n.{1}={2} SET n.{3}=null RETURN n"
        query = query.format(node_type, query_attribute, query_attribute_value, attribute_to_remove)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def add_relationship_attr(self, first_node_type, second_node_type, first_node_query_attr, first_node_query_value,
                              second_node_query_attr, second_node_query_value, relationship,
                              relationship_attributes):

        relationship_attributes_string = ", ".join(
            ["=".join(["r." + key, str(val)]) for key, val in relationship_attributes.items()])
        query = "MATCH (m: {0} {{ {1}:{2} }} )-[r:{3}]-(n: {4} {{ {5}:{6} }} ) SET {7}"
        query.format(first_node_type, relationship, first_node_query_attr, first_node_query_value, relationship,
                     second_node_type, second_node_query_attr, second_node_query_value,
                     relationship_attributes, relationship_attributes_string)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def delete_node_and_relationship(self, node_type, query_attribute, query_attribute_value):
        query = "MATCH (n: {0} {{ {1}: {2} }}) DETACH DELETE n"
        query = query.format(node_type, query_attribute, query_attribute_value)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def delete_node_only(self, node_type, query_attribute, query_attribute_value):
        query = "MATCH (n: {0} {{ {1}: {2} }}) DELETE n"
        query = query.format(node_type, query_attribute, query_attribute_value)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def delete_relationship_between_nodes(self, first_node_type, first_node_query_attr, first_node_query_value,
                                          second_node_type, second_node_query_attr, second_node_query_value,
                                          relationship):
        query = "MATCH (m:{0} {{ {1}: {2} }})-[r:{3}]-(n:{2} {{ {4}:{5} }}) DELETE r"
        query = query.format(first_node_type, first_node_query_attr, first_node_query_value, relationship,
                             second_node_type, second_node_query_attr, second_node_query_value)
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def delete_all(self):
        query = "MATCH (n) DETACH DELETE n"
        print(query)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    ###
    def find_node(self, node_type, attribute_name, attribute_value):
        query = "MATCH (n: {0}) WHERE n.{1}={2} RETURN n"
        query = query.format(node_type, attribute_name, attribute_value)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def find_node_using_multiple_attributes(self, node_type, attributes_dictionary):
        query = "MATCH (n:{0} {{1}}) RETURN n"
        query = query.format(node_type, attributes_dictionary)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def find_node_limit_element(self, node_type, attribute_name, attribute_value, limit=1):
        query = "MATCH (n:{0}) WHERE n.{1}={2} RETURN n LIMIT {3}"
        query = query.format(node_type, attribute_name, attribute_value, limit)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def find_node_with_regex(self, node_type, attribute_name, attribute_value):
        query = "MATCH (n: {0}) WHERE n.{1}=~{2} RETURN n"
        query = query.format(node_type, attribute_name, attribute_value)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    def find_node_with_regex_with_limit(self, node_type, attribute_name, attribute_value, limit=1):
        query = "MATCH (n: {0}) WHERE n.{1}=~{2} RETURN n LIMIT {3}"
        query = query.format(node_type, attribute_name, attribute_value, limit)
        result = TransactionExecutor.execute_query_auto_commit(self._driver, query)
        return result

    """Helper methods"""

    def __depth(self, dictionary, level=0):
        if not isinstance(dictionary, dict) or not dictionary:
            return level
        return max(self.__depth(dictionary[k], level + 1) for k in dictionary)

    """Closing Connection"""

    def close(self):
        self._driver.close()


class TransactionExecutor(object):
    """TRANSACTION EXECUTION FUNCTIONS"""

    @staticmethod
    def execute_query_auto_commit(driver, query):
        try:
            with driver.session() as session:
                return session.run(query)
        except ServiceUnavailable:
            return False

    @staticmethod
    def execute_query_write_transaction_function(driver, query):
        try:
            with driver.session() as session:
                return session.write_transaction(query)
        except ServiceUnavailable:
            return False

    @staticmethod
    def execute_query_read_transaction_function(driver, query):
        try:
            with driver.session() as session:
                return session.read_transaction(query)
        except ServiceUnavailable:
            return False

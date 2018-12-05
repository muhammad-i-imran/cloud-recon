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

    def create_node(self, node_type, id_keys, label, node_attributes={}):
        ids_string = json.dumps({k: node_attributes.get(k, None) for k in id_keys})
        node_attributes_string = ", ".join(["=".join(["n." + key, str(val)]) for key, val in node_attributes.items()])
        query = "MERGE (n: {0}  {1} ON CREATE SET {2} ON MATCH SET {3} RETURN n"
        query = query.format(node_type, ids_string, node_attributes_string, node_attributes_string)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def create_relationship(self, source_node_type, target_node_type,
                            source_node_attr_value,
                            target_node_attr_value, source_node_attr_name,
                            target_node_attr_name, relationship,
                            relationship_attributes, is_source_attr_name_regex=False,
                            is_target_attr_name_regex=False):

        if not relationship:
            raise IllegalArgumentError("Please provide valid relationships.")

        dict_depth = self.__depth(dictionary=relationship_attributes, level=0)
        if dict_depth > 1:
            raise ValueError("Invalid JSON format. Attributes JSON should have depth 1.")

        if is_source_attr_name_regex:
            source_nodes = self._find_node_with_regex(source_node_type, source_node_attr_name, source_node_attr_value)
        else:
            source_nodes = self._find_node(source_node_type, source_node_attr_name, source_node_attr_value)

        if is_target_attr_name_regex:
            target_nodes = self._find_node_with_regex(target_node_type, target_node_attr_name, target_node_attr_value)
        else:
            target_nodes = self._find_node(target_node_type, target_node_attr_name, target_node_attr_value)

        for node1 in source_nodes:
            for node2 in target_nodes:
                query = """MATCH(m: {source_node_type} {attributes to match start node})
                MATCH(n:{target_node_type} {attributes to match end node}) 
                MERGE(m)-[r:relationshipName {relationship_attributes}]->(n) 
                return r"""
                query = query.format(source_node_type, source_node_attr_name, source_node_attr_value, target_node_type,
                                     target_node_attr_name, target_node_attr_value, relationship, relationship_attributes)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def replace_node_attr(self, node_type, node_name_attr, node_name, node_attributes):
        query = """MATCH (n: {node_type} {{ {node_name_attr}: {node_name} }}) 
        SET n = {node_attributes}
        RETURN n"""
        query = query.format(node_type, node_name_attr, node_name, node_attributes)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def remove_node_all_attr(self, node_type, node_name_attr, node_name):
        query = """MATCH (n: {node_type} {{ {node_name_attr}: {node_name} }}) 
                SET n = {{}}
                RETURN n"""
        query = query.format(node_type, node_name_attr, node_name)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def remove_node_attr(self, node_type, query_attribute, query_attribute_value, attribute_to_remove):
        query = """MATCH (n: {0} {{ {1}: {2} }}) 
                        SET n.{3} = null
                        RETURN n"""
        query = query.format(node_type, node, query_attribute, query_attribute_value, attribute_to_remove)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def add_relationship_attr(self, first_node_type, second_node_type, first_node_name, second_node_name, relationship,
                              relationship_attributes):
        query = ""
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def delete_node_and_relationship(self, node_type, query_attribute, query_attribute_value):
        query = "MATCH (n: {0} {{ {1}: {2} }}) DETACH DELETE n"
        query = query.format(node_type, query_attribute, query_attribute_value)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def delete_node_only(self, node_type, query_attribute, query_attribute_value):
        query = "MATCH (n: {0} {{ {1}: {2} }}) DELETE n"
        query = query.format(node_type, query_attribute, query_attribute_value)
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def delete_multiple_nodes(self, list_node_type_name_mapping):
        query = ""
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def delete_relationship_between_nodes(self, first_node_type, first_node_name, second_node_type, second_node_name,
                                          relationship, relationship_attributes):
        query = ""
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def delete_multiple_relationships(self, list_of_relationship_dict):
        query = ""
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def create_multiple_nodes(self, list_node_info):
        query = ""
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def create_multiple_relationships(self, list_relationship_info):
        query = ""
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    def delete_all(self):
        query = "MATCH (n) DETACH DELETE n"
        result = TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return result

    ###
    """Helper methods"""

    def _find_node(self, node_type, attribute_name, attribute_value):
        query = """MATCH (n: {0} {{ {1}: {2} }}) 
RETURN n"""
        query = query.format(node_type, attribute_name, attribute_value)
        result = TransactionExecutor.execute_query_read_transaction_function(self._driver, query)
        return result

    def _find_node_using_multiple_attributes(self, node_type, attributes_dictionary):
        query = """MATCH (n:{node_type} {{ {attribute_name}: {attribute_name} }}) 
RETURN n"""
        query = query.format()
        result = TransactionExecutor.execute_query_read_transaction_function(self._driver, query)
        return result

    def _find_node_limit_element(self, node_type, attribute_name, attribute_value, limit):
        query = """MATCH (n:{0} {{ {1}: {2} }}) 
RETURN n LIMIT {3}"""
        query = query.format(node_type, attribute_name, attribute_value, limit)
        result = TransactionExecutor.execute_query_read_transaction_function(self._driver, query)
        return result

    def _find_node_with_regex(self, node_type, attribute_name, attribute_value):
        query = """MATCH (n: {0}) 
        WHERE n.{1}=~{2} 
        RETURN n"""
        query = query.format(node_type, attribute_name, attribute_value)
        result = TransactionExecutor.execute_query_read_transaction_function(self._driver, query)
        return result

    def _find_node_with_regex_with_limit(self, node_type, attribute_name, attribute_value, limit):
        query = """MATCH (n: {0}) 
        WHERE n.{1}=~{2} 
        RETURN n
        LIMIT {3}"""
        query = query.format(node_type, attribute_name, attribute_value, limit)
        result = TransactionExecutor.execute_query_read_transaction_function(self._driver, query)
        return result

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


##test
obj = Neo4JApi.init_with_basic_auth(uri='bolt://localhost:7687/', user='neo4j', password=None)
# x=obj.get_all_node()

attrs = {"_info___addresses___testnet___0___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",
         "links___1___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",
         "addresses___testnet___0___addr": "10.0.41.10",
         "_info___OS-EXT-SRV-ATTR:hypervisor_hostname": "wally199.cit.tu-berlin.de",
         "addresses___testnet___1___addr": "10.0.42.11",
         "_info___addresses___testnet___1___OS-EXT-IPS:type": "floating", "flavor___links___0___rel": "bookmark",
         "_info___image": "", "_info___addresses___testnet___0___OS-EXT-IPS:type": "fixed",
         "addresses___testnet___0___OS-EXT-IPS:type": "fixed", "OS-EXT-AZ:availability_zone": "nova",
         "OS-EXT-STS:power_state": 1, "_info___OS-EXT-SRV-ATTR:host": "wally199",
         "id": "a0d5ccd9-55de-4971-ad35-403db50b6ef3", "_loaded": True, "image": "", "accessIPv4": "",
         "addresses___testnet___0___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f", "accessIPv6": "",
         "security_groups___0___name": "default", "created": "2018-11-27T12:41:11Z",
         "hostId": "72d089ae78083af3c0848b3f0b73912792385200762c6cce2b267b73", "_info___links___0___rel": "self",
         "_info___os-extended-volumes:volumes_attached___0___id": "b19f4784-203d-4e76-92a9-adbbf8e099f6",
         "OS-EXT-SRV-ATTR:hypervisor_hostname": "wally199.cit.tu-berlin.de",
         "addresses___testnet___1___OS-EXT-IPS:type": "floating", "addresses___testnet___0___version": 4,
         "key_name": "CITKey", "addresses___testnet___1___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",
         "config_drive": "", "links___0___rel": "self",
         "_info___hostId": "72d089ae78083af3c0848b3f0b73912792385200762c6cce2b267b73", "OS-EXT-STS:vm_state": "active",
         "_info___links___1___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",
         "_info___addresses___testnet___0___version": 4, "_info___OS-EXT-STS:vm_state": "active",
         "_info___OS-EXT-STS:power_state": 1, "_info___key_name": "CITKey",
         "user_id": "0ac3fffca5b44975b3f75adb355675d7", "OS-EXT-SRV-ATTR:instance_name": "instance-00000013",
         "name": "new_instance",
         "links___0___href": "http://130.149.249.187:8774/v2.1/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",
         "updated": "2018-11-27T12:45:38Z", "status": "ACTIVE", "tenant_id": "e5821398aa674ceca59cf0c142bb226d",
         "addresses___testnet___1___version": 4, "_info___security_groups___1___name": "allopen",
         "os-extended-volumes:volumes_attached___0___id": "b19f4784-203d-4e76-92a9-adbbf8e099f6",
         "_info___id": "a0d5ccd9-55de-4971-ad35-403db50b6ef3",
         "_info___OS-EXT-SRV-ATTR:instance_name": "instance-00000013", "_info___status": "ACTIVE",
         "_info___tenant_id": "e5821398aa674ceca59cf0c142bb226d", "OS-DCF:diskConfig": "AUTO",
         "_info___flavor___id": "3", "_info___security_groups___0___name": "default", "links___1___rel": "bookmark",
         "_info___addresses___testnet___1___addr": "10.0.42.11", "_info___addresses___testnet___0___addr": "10.0.41.10",
         "_info___OS-EXT-AZ:availability_zone": "nova", "_info___addresses___testnet___1___version": 4,
         "OS-EXT-SRV-ATTR:host": "wally199", "security_groups___1___name": "allopen",
         "_info___OS-SRV-USG:launched_at": "2018-11-27T12:42:13.000000", "_info___OS-DCF:diskConfig": "AUTO",
         "flavor___id": "3", "_info___user_id": "0ac3fffca5b44975b3f75adb355675d7",
         "_info___flavor___links___0___rel": "bookmark", "_info___created": "2018-11-27T12:41:11Z",
         "_info___addresses___testnet___1___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",
         "_info___links___1___rel": "bookmark",
         "_info___links___0___href": "http://130.149.249.187:8774/v2.1/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",
         "_info___name": "new_instance", "_info___updated": "2018-11-27T12:45:38Z", "_info___accessIPv6": "",
         "_info___flavor___links___0___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/flavors/3",
         "_info___config_drive": "", "progress": 0, "OS-SRV-USG:launched_at": "2018-11-27T12:42:13.000000",
         "flavor___links___0___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/flavors/3",
         "_info___progress": 0, "_info___accessIPv4": ""}
x = obj.create_node("SERVER", ["id"], "VM1", attrs)

for rec in x:
    for node in rec:
        for key in node:
            print(str(key) + ": " + node[key])

from neo4j.v1 import GraphDatabase, Session, ServiceUnavailable, custom_auth, TRUST_ALL_CERTIFICATES
import json


def __depth(self, dictionary, level=0):
    if not isinstance(dictionary, dict) or not dictionary:
        return level
    return max(self.__depth(dictionary[k], level + 1) for k in dictionary)

class Neo4JApi(object):
    def __init__(self, uri, **parameters):
        self._driver = GraphDatabase.driver(uri=uri, **parameters)

    """ 'OVERLOADED' CONSTRUCTORS """

    ### TODO: Connection pool management
    @classmethod
    def init_with_basic_auth(cls, uri, user, password, encrypted=True, connection_timeout=30, max_retry_time=10, trust=TRUST_ALL_CERTIFICATES):
        return cls(uri, auth=(user, password), encrypted=encrypted, connection_timeout=connection_timeout,
                   max_retry_time=max_retry_time, trust=trust)

    @classmethod
    def init_with_kerberos_auth(cls, uri, ticket, encrypted=True, connection_timeout=30, max_retry_time=10, trust=TRUST_ALL_CERTIFICATES):
        return cls(uri, auth=(ticket), encrypted=encrypted, connection_timeout=connection_timeout,
                   max_retry_time=max_retry_time, trust=trust)

    @classmethod
    def init_with_custom_auth(cls, uri, principal, credentials, realm, scheme, encrypted=True, connection_timeout=30, max_retry_time=10, trust=TRUST_ALL_CERTIFICATES, **parameters):
        return cls(uri, auth=custom_auth(principal, credentials, realm, scheme, **parameters), encrypted=encrypted, connection_timeout=connection_timeout,
                   max_retry_time=max_retry_time, trust=trust)

    """CRUD Operations"""
    """All transactions are auto-commit"""

    def get_all_node(self):
        query = "MATCH (n) RETURN n"
        TransactionExecutor.execute_query_read_transaction_function(self._driver, query)

    def create_node(self, node_type, id_keys, label, node_attributes={}):
        ids_string = json.dumps({k: node_attributes.get(k, None) for k in id_keys})
        node_attributes_string = ", ".join(["=".join(["n." + key, str(val)]) for key, val in node_attributes.items()])

        query = "MERGE (n:" + node_type + " "+ ids_string +" " \
                "ON CREATE SET " + node_attributes_string + "" \
                "ON MATCH SET " + node_attributes_string + "" \
                "RETURN n"
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

    def create_relationship(self, source_node_type, target_node_type,
                            source_node_attr_value,
                            target_node_attr_value, source_node_attr_name,
                            target_node_attr_name, relationship,
                            relationship_attributes, is_source_attr_name_regex=False,
                            is_target_attr_name_regex=False):

        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def add_node_attr(self, node_type, node_name, node_attributes):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return

    def add_relationship_attr(self, first_node_type, second_node_type, first_node_name, second_node_name, relationship,
                              relationship_attributes):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def delete_node(self, node_type, node_name):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def delete_multiple_nodes(self, list_node_type_name_mapping):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def delete_relationship_between_nodes(self, first_node_type, first_node_name, second_node_type, second_node_name,
                                          relationship, relationship_attributes):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)
        return

    def delete_multiple_relationships(self, list_of_relationship_dict):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def create_multiple_nodes(self, list_node_info):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def create_multiple_relationships(self, list_relationship_info):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    def delete_all(self):
        TransactionExecutor.execute_query_write_transaction_function(self._driver, query)

        return

    ###
    """Helper methods"""

    def _create_cypher_statement(self):

        return ""

    def _find_node(self, element_type, attribute_name, attribute_value):
        TransactionExecutor.execute_query_read_transaction_function(self._driver, query)

        return

    ###
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
        # except:
        #     return

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

attrs = {  "_info___addresses___testnet___0___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",  "links___1___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",  "addresses___testnet___0___addr": "10.0.41.10",  "_info___OS-EXT-SRV-ATTR:hypervisor_hostname": "wally199.cit.tu-berlin.de",  "addresses___testnet___1___addr": "10.0.42.11",  "_info___addresses___testnet___1___OS-EXT-IPS:type": "floating",  "flavor___links___0___rel": "bookmark",  "_info___image": "",  "_info___addresses___testnet___0___OS-EXT-IPS:type": "fixed",  "addresses___testnet___0___OS-EXT-IPS:type": "fixed",  "OS-EXT-AZ:availability_zone": "nova",  "OS-EXT-STS:power_state": 1,  "_info___OS-EXT-SRV-ATTR:host": "wally199",  "id": "a0d5ccd9-55de-4971-ad35-403db50b6ef3",  "_loaded": True,  "image": "",  "accessIPv4": "",  "addresses___testnet___0___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",  "accessIPv6": "",  "security_groups___0___name": "default",  "created": "2018-11-27T12:41:11Z",  "hostId": "72d089ae78083af3c0848b3f0b73912792385200762c6cce2b267b73",  "_info___links___0___rel": "self",  "_info___os-extended-volumes:volumes_attached___0___id": "b19f4784-203d-4e76-92a9-adbbf8e099f6",  "OS-EXT-SRV-ATTR:hypervisor_hostname": "wally199.cit.tu-berlin.de",  "addresses___testnet___1___OS-EXT-IPS:type": "floating",  "addresses___testnet___0___version": 4,  "key_name": "CITKey",  "addresses___testnet___1___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",  "config_drive": "",  "links___0___rel": "self",  "_info___hostId": "72d089ae78083af3c0848b3f0b73912792385200762c6cce2b267b73",  "OS-EXT-STS:vm_state": "active",  "_info___links___1___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",  "_info___addresses___testnet___0___version": 4,  "_info___OS-EXT-STS:vm_state": "active",  "_info___OS-EXT-STS:power_state": 1,  "_info___key_name": "CITKey",  "user_id": "0ac3fffca5b44975b3f75adb355675d7",  "OS-EXT-SRV-ATTR:instance_name": "instance-00000013",  "name": "new_instance",  "links___0___href": "http://130.149.249.187:8774/v2.1/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",  "updated": "2018-11-27T12:45:38Z",  "status": "ACTIVE",  "tenant_id": "e5821398aa674ceca59cf0c142bb226d",  "addresses___testnet___1___version": 4,  "_info___security_groups___1___name": "allopen",  "os-extended-volumes:volumes_attached___0___id": "b19f4784-203d-4e76-92a9-adbbf8e099f6",  "_info___id": "a0d5ccd9-55de-4971-ad35-403db50b6ef3",  "_info___OS-EXT-SRV-ATTR:instance_name": "instance-00000013",  "_info___status": "ACTIVE",  "_info___tenant_id": "e5821398aa674ceca59cf0c142bb226d",  "OS-DCF:diskConfig": "AUTO",  "_info___flavor___id": "3",  "_info___security_groups___0___name": "default",  "links___1___rel": "bookmark",  "_info___addresses___testnet___1___addr": "10.0.42.11",  "_info___addresses___testnet___0___addr": "10.0.41.10",  "_info___OS-EXT-AZ:availability_zone": "nova",  "_info___addresses___testnet___1___version": 4,  "OS-EXT-SRV-ATTR:host": "wally199",  "security_groups___1___name": "allopen",  "_info___OS-SRV-USG:launched_at": "2018-11-27T12:42:13.000000",  "_info___OS-DCF:diskConfig": "AUTO",  "flavor___id": "3",  "_info___user_id": "0ac3fffca5b44975b3f75adb355675d7",  "_info___flavor___links___0___rel": "bookmark",  "_info___created": "2018-11-27T12:41:11Z",  "_info___addresses___testnet___1___OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:f8:38:2f",  "_info___links___1___rel": "bookmark",  "_info___links___0___href": "http://130.149.249.187:8774/v2.1/e5821398aa674ceca59cf0c142bb226d/servers/a0d5ccd9-55de-4971-ad35-403db50b6ef3",  "_info___name": "new_instance",  "_info___updated": "2018-11-27T12:45:38Z",  "_info___accessIPv6": "",  "_info___flavor___links___0___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/flavors/3",  "_info___config_drive": "",  "progress": 0,  "OS-SRV-USG:launched_at": "2018-11-27T12:42:13.000000",  "flavor___links___0___href": "http://130.149.249.187:8774/e5821398aa674ceca59cf0c142bb226d/flavors/3",  "_info___progress": 0,  "_info___accessIPv4": ""}
x=obj.create_node("SERVER", ["id"], "VM1", attrs)

for rec in x:
    for node in rec:
        for key in node:
            print(str(key) + ": " + node[key])
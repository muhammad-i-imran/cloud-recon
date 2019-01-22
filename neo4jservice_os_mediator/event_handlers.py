# from node_manager import NodeManager
#
# class NotificationEventHandlers(object):
#
#     @staticmethod
#     def delete_server(cls, node_type, payload):
#         attribute_name=openstack_info[node_type]['id_key']
#         attribute_value=payload['instance_id']
#         NodeManager.delete_node(node_type, attribute_name, attribute_value)
#
#     @staticmethod
#     def update_server(cls, node_type, payload):
#         attribute_name = oenstack_info[node_type]['id_key']
#         attribute_value = payload['instance_id']
#         NodeManager.update_node(node_type, attribute_name, attribute_value)
#
#     @staticmethod
#     def delete_network(cls, node_type, payload):
#         raise NotImplementedError("not implemented yet")
#
#
#     @staticmethod
#     def update_network(cls, node_type, payload):
#         raise NotImplementedError("not implemented yet")
#
#     @staticmethod
#     def create_container(cls, node_type, payload):
#         raise NotImplementedError("not implemented yet")
#
#     @staticmethod
#     def delete_container(cls, node_type, payload):
#         raise NotImplementedError("not implemented yet")
#
#     @staticmethod
#     def update_container(cls, node_type, payload):
#         raise NotImplementedError("not implemented yet")


from graphelementsdispatcher.node_manager import *
from utils import *

def notifier_callback(event_type, payload):
    # TODO: Compare graph data with openstack data and update node if different
    openstack_component = NodeManager.get_node_by_properties(
        {'id': payload['id']})  # get openstack node data using apis
    openstack_component_flattened_dict = get_flattened_dictionary(openstack_component)
    node_in_db = NodeManager.get_node_by_properties(
        {'id': payload['id']})  # will receive data that is already flattened when inserted
    if not diff_dictionaries(node_in_db,
                             openstack_component_flattened_dict):  # if dictionaries are different then update, otherwise ignore
        NodeManager.update_node(node_in_db, )

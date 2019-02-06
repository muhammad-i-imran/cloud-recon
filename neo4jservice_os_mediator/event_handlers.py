from graphelementsdispatcher.node_manager import *
from utils import *


def notifier_callback(event_type, payload):
    # TODO: Compare graph data with openstack data and update node if different
    openstack_component = None  # get openstack node data using querier

    openstack_component_flattened_dict = get_flattened_dictionary(openstack_component)
    node_in_db = NodeManager.get_node_by_properties(
        {'id': payload['id']})  # will receive data that is already flattened when inserted
    if not diff_dictionaries(node_in_db, openstack_component_flattened_dict):  # if dictionaries are different then update, otherwise ignore
        NodeManager.update_node(node_in_db, ) #TODO: what if the event is delete? or other than update?

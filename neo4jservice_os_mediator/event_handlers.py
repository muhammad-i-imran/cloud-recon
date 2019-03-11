from graphelementsdispatcher.node_manager import *
from utils import *
import node_data_assembler


delete_events=[]
create_or_update_events=[]
def notifier_callback(event_type, payload):
    # TODO: Compare graph data with openstack data and update node if different

    print("Handling notifications...")

    if event_type in delete_events:
        data = {}
        data['node_type']='SERVERS' # get corresponding label
        data['node_properties']= payload['instance_id']
        NodeManager.delete_nodes(data)
    else:
        #update or create: update using node creation node
        #fetch component from openstack
        data={}
        node_type="SERVERS" # get corresponding label
        node_type_with_prefix = envvars.GRAPH_ELEMENT_TYPE_PREFIX + node_type
        function_name = "".join(["create_", node_type]) # create is used, becuse even if the node already exist, the method implemented in REST service will merge with the existing one.
        function_to_call = getattr(node_data_assembler, function_name.lower())
        function_to_call(node_type=node_type_with_prefix, label_key=cloud_config_info[node_type]['name_attr'], id_key=cloud_config_info[node_type]['id_key'])

        # openstack_component_flattened_dict = get_flattened_dictionary(openstack_data)
        # node_in_db = NodeManager.get_node_by_properties({'id': payload['instance_id']})  # will receive data that is already flattened when inserted

        # if not diff_dictionaries(node_in_db, openstack_component_flattened_dict):  # if dictionaries are different then update, otherwise ignore
        #     NodeManager.update_node(node_in_db, )


    return


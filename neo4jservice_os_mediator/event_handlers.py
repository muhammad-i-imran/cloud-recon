from graphelementsdispatcher.node_manager import *
from utils import *
import node_data_assembler

event_component_mappings = json.loads(open(envvars.COMPONENT_EVENT_MAPPING_FILE).read())
configuratons = json.loads(open(envvars.CONFIG_FILE_PATH).read())
cloud_provider = configuratons["cloud_provider"]
cloud_config_info = configuratons["cloud_config_info"]

def notifier_callback(event_type, payload):
    print("######################################################################")
    print(event_type)
    print(payload)
    print("######################################################################")

    event_info = event_component_mappings[event_type]
    event_component_type = event_info['component']  # e.g. SERVERS, IMAGES, etc.
    event_operation = event_info['operation']  # e.g. U: update, D:delete, C: create
    # component_id_property_in_payload = event_info['component_id_property_in_payload'] #todo:

    if event_operation == 'D':
        data = {}
        data['node_type'] = event_component_type
        data['node_properties'] = payload[
            'instance_id']  # todo: check for all events' payloads. if they all have similar property name, then it's fine. oterhwise, include that in the json file also
        NodeManager.delete_nodes(data)
    elif event_operation == 'C' or event_operation == 'U':
        # update or create: update using node creation node
        # fetch component from openstack

        node_type = event_component_type  # get corresponding label
        search_opts = {}
        search_opts[cloud_config_info[node_type]['id_key']] = payload[
            'instance_id']  # todo: check for all events' payloads. if they all have similar property name, then it's fine. oterhwise, include that in the json file also

        node_type_with_prefix = envvars.GRAPH_ELEMENT_TYPE_PREFIX + node_type
        function_name = "".join(["create_",
                                 node_type])  # create is used, becuse even if the node already exist, the method implemented in REST service will merge with the existing one.
        function_to_call = getattr(node_data_assembler, function_name.lower())
        function_to_call(node_type=node_type_with_prefix, label_key=cloud_config_info[node_type]['name_attr'],
                         id_key=cloud_config_info[node_type]['id_key'], search_opts=search_opts)
    else:
        raise Exception("Operation not known. Please select C for Create, D for Delete, or U for Update opeerations.")
    return
import node_data_assembler
from utils import *

event_component_mappings = json.loads(open(envvars.COMPONENT_EVENT_MAPPING_FILE).read())
configuratons = json.loads(open(envvars.CONFIG_FILE_PATH).read())
cloud_provider = configuratons["cloud_provider"]
cloud_config_info = configuratons["cloud_config_info"]


def notifier_callback(event_type, payload):
    print("==================================================")
    print("Handling event: %s" % event_type)
    print(payload)

    #todo: update relationship after a node's creation, updation, deletion...

    try:
        event_info = event_component_mappings[event_type]
    except KeyError as err:
        print("KeyError occured while reading event type from event_component_mappings: %s" % str(err))
    except Exception as ex:
        print("Exception occured while reading event type from event_component_mappings: %s" % str(ex))
    else:
        event_component_type = event_info['component']  # e.g. SERVERS, IMAGES, etc.
        event_operation = event_info['operation']  # e.g. U: update, D:delete, C: create
        component_id_property_in_payload = event_info['component_id_property_in_payload']
        if event_operation == 'D':
            data = {}
            try:
                data['node_type'] = event_component_type
                data['node_properties'] = payload[component_id_property_in_payload]
                NodeManager.delete_nodes(data)
            except KeyError as err:
                print("KeyError occured while reading key (%s) from payload" % str(err))
            except Exception as ex:
                print("Exception occurred while performing delete node operation against an event. Exception message: %s" % str(ex))
        elif event_operation == 'C' or event_operation == 'U':
            node_type = event_component_type  # get corresponding label
            try:
                search_opts = {}
                search_opts[cloud_config_info[node_type]['id_key']] = payload[
                    component_id_property_in_payload]  # query only that single element
                node_type_with_prefix = envvars.GRAPH_ELEMENT_TYPE_PREFIX + node_type
                function_name = "".join(["create_",
                                         node_type])  # create is used, becuse even if the node already exist, the method implemented in REST service will merge with the existing one.
                function_to_call = getattr(node_data_assembler, function_name.lower())
                function_to_call(node_type=node_type_with_prefix, label_key=cloud_config_info[node_type]['name_attr'],
                                 id_key=cloud_config_info[node_type]['id_key'], search_opts=search_opts)
            except KeyError as err:
                print("KeyError occured while reading key. Error message: %s" % str(err))
            except Exception as ex:
                print("Exception occurred while performing Create or Update node operation against an event. Exception message: %s" % str(ex))
        else:
            raise Exception(
                "Operation not known. Please select C for Create, D for Delete, or U for Update operations.")
    return

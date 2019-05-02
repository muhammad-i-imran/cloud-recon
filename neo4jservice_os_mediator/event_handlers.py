import node_data_assembler
from graphelementsdispatcher.node_manager import NodeManager
from graphelementsdispatcher.relationship_manager import RelationshipManager
from utils import *
from logging_config import Logger
import openstack_preprocessor

from functools import reduce
import operator


logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL,
                logger_name=os.path.basename(__file__)).logger

event_component_mappings = json.loads(open(envvars.COMPONENT_EVENT_MAPPING_FILE).read())
configuratons = json.loads(open(envvars.CONFIG_FILE_PATH).read())
cloud_provider = configuratons["cloud_provider"]
cloud_config_info = configuratons["cloud_config_info"]

##-------------------------------------------------------------------------
def get_value_from_dict(payload_dict:dict, keys_list:list):
    return reduce(operator.getitem, keys_list, payload_dict)

##-------------------------------------------------------------------------


def notifier_callback(event_type:str, payload:dict):
    logger.info("Handling event: {0}".format(event_type))
    logger.debug("Payload: {0}".format(str(payload)))

    try:
        event_info = event_component_mappings[event_type]
    except KeyError as err:
        logger.error("KeyError occured while reading event type from event_component_mappings: {0}".format(str(err)))
    except Exception as ex:
        logger.error("Exception occured while reading event type from event_component_mappings: {0}".format(str(ex)))
    else:
        node_type = event_info['component']  # e.g. SERVERS, IMAGES, etc.
        graph_element = event_info['graph_element']  # e.g. N for Node, R for relationship. type: list
        event_operation = event_info['operation']  # e.g. U: update, D:delete, C: create
        component_id_property_in_payload = event_info['component_id_property_in_payload']
        if event_operation == 'D':
            data = {}
            try:
                if "N" in graph_element:
                    data['node_type'] = node_type
                    data['node_properties'] = {}
                    data['node_properties'][cloud_config_info[node_type]['id_key']] = get_value_from_dict(payload, payload[component_id_property_in_payload]) # payload[component_id_property_in_payload] is a dict now. because id may be at a nested level in the payload
                    logger.info(
                        "Trying to delete the node's relationships and the node itself (node type: {0}, node id: {1}) in graph.".format(data['node_type'], data[
                            'node_properties']))
                    RelationshipManager.delete_node_all_relationships(data)
                    NodeManager.delete_nodes(data)
            except KeyError as err:
                logger.error("KeyError occured while reading key ({0}) from payload".format(str(err)))
            except Exception as ex:
                logger.error(
                    "Exception occurred while performing delete node operation against an event. Exception message: {0}".format(
                        str(ex)))
        elif event_operation == 'C' or event_operation == 'U':
            try:
                if "N" in graph_element:  # if the event affects node
                    search_opts = {}
                    search_opts[cloud_config_info[node_type]['id_key']] = get_value_from_dict(payload, payload[component_id_property_in_payload]) # payload[component_id_property_in_payload] is a dict now. because id may be at a nested level in the payload

                    logger.info("Trying to create or update node in graph.")
                    creator = node_data_assembler.NodeCreator()
                    function_to_call = openstack_preprocessor._get_function_for_element(element_type=node_type,
                                                                                        creator=creator)
                    if node_type == "CONTAINERS":
                        function_to_call(node_type=node_type,
                                         node_secondary_labels=cloud_config_info[node_type]['node_secondary_labels'],
                                         label_key=cloud_config_info[node_type]['name_attr'],
                                         id_key=cloud_config_info[node_type]['id_key'], data=payload)
                    else:
                        function_to_call(node_type=node_type,
                                         node_secondary_labels=cloud_config_info[node_type]['node_secondary_labels'],
                                         label_key=cloud_config_info[node_type]['name_attr'],
                                         id_key=cloud_config_info[node_type]['id_key'], search_opts=search_opts)
                if "R" in graph_element:  # if the event affects relationship between nodes
                    if event_operation == 'U':
                        # remove node's all relationships if it is an update operation
                        data = {}
                        data['node_type'] = node_type
                        data['node_properties'] = {}
                        data['node_properties'][cloud_config_info[node_type]['id_key']] = get_value_from_dict(payload, payload[component_id_property_in_payload]) # payload[component_id_property_in_payload] is a dict now. because id may be at a nested level in the payload
                        RelationshipManager.delete_node_all_relationships(data)

                    for relationship in event_info["relationships"]:
                        logger.info("Trying to create/update relationship(s) among nodes.")

                        source_node_properties = {}  # source node is the node for which the event is currently received
                        source_node_properties[relationship["source_property_name_in_db"]] = get_value_from_dict(payload, payload[component_id_property_in_payload]) # payload[component_id_property_in_payload] is a dict now. because id may be at a nested level in the payload

                        target_node_properties = {}  # target node is the node which is affect by the the event is currently received
                        target_node_properties[relationship["target_property_name_in_db"]] = get_value_from_dict(payload, payload[
                            relationship["target_node_type_id_in_payload"]]) # payload[relationship["target_node_type_id_in_payload"]] is a dict now. because id may be at a nested level in the payload


                        relationship_data = {}
                        relationship_data["source_node_type"] = node_type
                        relationship_data["source_node_properties"] = source_node_properties
                        relationship_data["target_node_type"] = relationship['target_node_type']
                        relationship_data["target_node_properties"] = target_node_properties
                        relationship_data["relationship"] = relationship["relationship"]
                        relationship_data["relationship_properties"] = relationship["relationship_properties"]
                        RelationshipManager.create_relationship(relationship_data)
            except KeyError as err:
                logger.error("KeyError occured while reading key. Error message: {0}".format(str(err)))
            except Exception as ex:
                logger.error(
                    "Exception occurred while performing Create or Update node operation against an event. Exception message: {0}".format(
                        str(ex)))
        else:
            logger.error("Operation not known. Please select C for Create, D for Delete, or U for Update operations.")
            raise Exception(
                "Operation not known. Please select C for Create, D for Delete, or U for Update operations.")

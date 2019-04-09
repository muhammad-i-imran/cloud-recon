import node_data_assembler
from utils import *
from logging_config import Logger

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

event_component_mappings = json.loads(open(envvars.COMPONENT_EVENT_MAPPING_FILE).read())
configuratons = json.loads(open(envvars.CONFIG_FILE_PATH).read())
cloud_provider = configuratons["cloud_provider"]
cloud_config_info = configuratons["cloud_config_info"]



def notifier_callback(event_type, payload):
    logger.info("Handling event: %s" % event_type)
    logger.debug(str(payload))

    #todo: update relationship after a node's creation, updation, deletion...

    try:
        event_info = event_component_mappings[event_type]
    except KeyError as err:
        logger.error("KeyError occured while reading event type from event_component_mappings: %s" % str(err))
    except Exception as ex:
        logger.error("Exception occured while reading event type from event_component_mappings: %s" % str(ex))
    else:
        event_component_type = event_info['component']  # e.g. SERVERS, IMAGES, etc.
        event_operation = event_info['operation']  # e.g. U: update, D:delete, C: create
        component_id_property_in_payload = event_info['component_id_property_in_payload']
        if event_operation == 'D':
            data = {}
            try:
                data['node_type'] = event_component_type
                data['node_properties'] = payload[component_id_property_in_payload]
                logger.info("Trying to delete node (node type: %s, node id: %s) in graph." % data['node_type'], data['node_properties'])
                NodeManager.delete_nodes(data)
            except KeyError as err:
                logger.error("KeyError occured while reading key (%s) from payload" % str(err))
            except Exception as ex:
                logger.error("Exception occurred while performing delete node operation against an event. Exception message: %s" % str(ex))
        elif event_operation == 'C' or event_operation == 'U':
            node_type = event_component_type  # get corresponding label
            try:
                search_opts = {}
                search_opts[cloud_config_info[node_type]['id_key']] = payload[
                    component_id_property_in_payload]  # query only that single element
                function_name = "".join(["create_",
                                         node_type])  # create is used, becuse even if the node already exist, the method implemented in REST service will merge with the existing one.
                function_to_call = getattr(node_data_assembler, function_name.lower())
                logger.info("Trying to create or update node in graph.")
                function_to_call(node_type=node_type, node_secondary_labels=cloud_config_info[node_type]['node_secondary_labels'],  label_key=cloud_config_info[node_type]['name_attr'],
                                 id_key=cloud_config_info[node_type]['id_key'], search_opts=search_opts)
            except KeyError as err:
                logger.error("KeyError occured while reading key. Error message: %s" % str(err))
            except Exception as ex:
                logger.error("Exception occurred while performing Create or Update node operation against an event. Exception message: %s" % str(ex))
        else:
            logger.error("Operation not known. Please select C for Create, D for Delete, or U for Update operations.")
            raise Exception(
                "Operation not known. Please select C for Create, D for Delete, or U for Update operations.")
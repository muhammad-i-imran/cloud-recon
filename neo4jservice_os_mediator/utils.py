import json
import os
from flatten_json import flatten
import envvars
from logging_config import Logger


logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

"""
This file contains general-purpose functions to be used across the module
"""


def get_flattened_dictionary(dict: dict, separator='___'):
    """

    :param dict:
    :param separator:
    :return:
    """
    logger.info("Flattening dictionary.")
    return flatten(dict, separator=separator)

def  compare_data(graph_data: list, openstack_data: list, comparison_properties: list):
    """

    :param graph_data_dict: dict that's fetched from the graph db
    :param openstack_data_dict: dict that's fetched from openstack
    :param comparison_keys:  key(s) on which we have to compare two records to know if they are matched
    :return: array of dicts that don't match

    """
    non_matched_data = []
    for graph_rec in graph_data:
        has_rec_matched = False

        logger.debug("Finding if the record is staled.")
        logger.debug("Record type is: {0}.".format(type(graph_rec)))

        for openstack_rec in openstack_data:
            has_attrs_matched  = False
            for key in comparison_properties:
                try:
                    if graph_rec[key] == openstack_rec[key]:
                        has_attrs_matched = True
                    else:
                        has_attrs_matched = False
                        break
                except Exception as ex:
                    logger.error("Exception occurred while comparing OpenStack and Graph DB records. Exception message: {0}.".format(str(ex)))

            if has_attrs_matched:
                has_rec_matched = True
                break
        if not has_rec_matched:
            logger.debug("Found stale record. Now appending it to a list.")
            non_matched_data.append(graph_rec)
    return non_matched_data

def prepare_node_data(data_list, node_type, node_secondary_labels, label_key='name', id_key="id"):
    """

    :param data_list:
    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    logger.info("Preparing node data for node type %s." % node_type)
    nodes_data = []
    for i in data_list:
        info = i if type(i) is dict else i.__dict__
        # label = info.pop(label_key, None)
        if label_key != 'name':
            info['name'] = info[
                label_key]  # property with name 'name' is important for displaying (as a label on node) purpose
            del info[label_key]

        # remove non-serializable elements
        logger.debug("Trying to convert strings to Json and remove non-serializable elements.")
        for key in list(info):
            try:
                json.dumps(info[key])
            except Exception as ex:
                del info[key]

        flattened_info_dict = get_flattened_dictionary(info)

        node_data = {}
        node_data["id_key"] = id_key
        node_data["node_type"] = node_type
        node_data["node_secondary_labels"] = node_secondary_labels
        node_data["node_properties"] = flattened_info_dict
        nodes_data.append(node_data)
    logger.debug("Returning prepared nodes for type %s." % node_type)
    return nodes_data
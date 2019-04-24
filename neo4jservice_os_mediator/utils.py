import json
import os
import re

from flatten_json import flatten

import envvars
from graphelementsdispatcher.node_manager import NodeManager
from openstackqueryapi.queryos import ShellCommandExecutor

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


# def diff_dictionaries(neoj_data, openstack_data):
#     """
#
#     :param neoj_data:
#     :param openstack_data:
#     :return:
#     """
#     for k in neoj_data:
#         if k in openstack_data:
#             if neoj_data[k] != openstack_data[k]:
#                 return False
#         else:
#             return False
#     return True


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
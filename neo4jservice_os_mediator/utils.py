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


# def add_prefix_to_dict_keys(dictionary, prefix_string=""):
#     """
#
#     :param dictionary:
#     :param prefix_string:
#     :return:
#     """
#     if not prefix_string:
#         return dictionary
#     new_dictionary = {}
#     keys = dictionary.keys()
#     for key in keys:
#         new_key = prefix_string + key
#         new_dictionary[new_key] = dictionary[key]
#         del dictionary[key]
#     return new_dictionary


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


def server_command_initiator(server_ip, private_key_path, vm_username):
    """

    :param server_ip:
    :param private_key_path:
    :param vm_username:
    :return:
    """
    logger.info("Preparing and initiating command for fetching Docker Containers.")
    if not os.path.exists(private_key_path):
        logger.error("Exception occured: Private key files path not found.")
        raise Exception("Exception occured: Private key files path not found.")

    command = "sudo docker ps --format \"{{json .}}\""
    ssh_cmd_executor = ShellCommandExecutor()
    try:
        logger.info("Trying to connect VM using IP {0} and user name {1}".format(server_ip, vm_username))
        ssh_cmd_executor.connect(ip=server_ip, username=vm_username, private_key_file_path=private_key_path)
    except Exception as e:
        logger.error("Exception occured: {0}".format(str(e)))
        return

    try:
        logger.debug("Reading output received from Docker.")
        stdin, stdout, stderr = ssh_cmd_executor.execute_command(command)
    except Exception as ex:
        logger.error("Exception occured: %s" % str(ex))
    else:
        logger.debug("Reading output received from Docker.")
        containers_string_info = stdout.readlines()
        containers_list = []
        for c in containers_string_info:
            container_info_dict = {}
            container_info = json.loads(c)
            container_info_dict["id"] = container_info["ID"]
            container_info_dict["container_name"] = container_info["Names"]
            container_info_dict["name"] = container_info["Image"]
            container_info_dict["ports"] = container_info["Ports"]
            container_info_dict["networks"] = container_info["Networks"]
            container_info_dict["mounts"] = container_info["Mounts"]
            containers_list.append(container_info_dict)
        try:
            logger.info("Closing connection to the VM.")
            ssh_cmd_executor.close_connection()
        except Exception as ex:
            logger.error("Exception occured: %s" % str(ex))
        return containers_list


def fetch_and_prepare_container_nodes(node_type):
    """

    :param node_type:
    :param server_name_attr:
    :param private_keys_folder:
    :param vm_username:
    :return:
    """
    logger.info("Fetching and preparing Docker container nodes.")
    query = {}
    query["node_type"] = 'SERVERS'

    containers_list = []

    try:
        logger.info("Getting nodes from graph database using query %s." % str(query))
        servers = NodeManager.get_nodes(query)
    except Exception as ex:
        logger.error("Exception occured: %s" % str(ex))
    else:
        for server in servers:
            user_name= server[
                'key_name']  # not sure, whether iterate throuhg all keys or current user keys or the vm creator keys???
            ips = [value for key, value in server.items() if
                   re.match("^addresses.*?addr$", key)]  # "addresses___test-net___1___addr":"10.0.42.17", parse this
            server_id = server["id"]
            server_name = server["name"]
            private_key_path = os.path.join(envvars.PRIVATE_KEYS_FOLDER, user_name)

            if not os.path.exists(private_key_path):
                logger.warn("Private key file for user {0} not available at path {1}." .format(user_name, private_key_path))
                continue
            # also check if ip is of valid format... ()using regex

            for ip in ips:
                try:
                    logger.debug("Calling 'server_command_initiator' function.")
                    containers = server_command_initiator(server_ip=ip, private_key_path=private_key_path,
                                                          vm_username=envvars.VM_USERNAME)
                    logger.debug("Received zero or more containers from 'server_command_initiator'.")
                    if containers:
                        if len(containers) > 0:
                            containers_list = containers
                            break
                except Exception as ex:
                    logger.error("Exception occured: %s" % str(ex))
                    pass
                else:
                    continue

            for container in containers_list:
                container["server_name"] = server_name
                container["server_id"] = server_id
    return containers_list  ##TODO: yield containers's list for each server instead of all containers
import json
from openstackqueryapi.queryos import ShellCommandExecutor
import os
from node_data_assembler import fetch_servers

"""
This file contains general-purpose functions to be used across the module
"""


def get_flattened_dictionary(dict, separator='___'):
    from flatten_json import flatten
    return flatten(dict, separator=separator)


def diff_dictionaries(neoj_data, openstack_data):
    for  k in neoj_data:
        if k in openstack_data:
            if neoj_data[k] != openstack_data[k]:
                return False
        else:
            return False
    return True

def add_prefix_to_dict_keys(dictionary, prefix_string=""):
    if not prefix_string:
        return dictionary
    new_dictionary={}
    keys = dictionary.keys()
    for key in keys:
        new_key = prefix_string + key
        new_dictionary[new_key] = dictionary[key]
        del dictionary[key]
    return new_dictionary


def prepare_node_data(data_list, node_type, label_key='name', id_key="id"):
    """

    :param data_list:
    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    nodes_data = []
    for i in data_list:
        info = i if type(i) is dict else i.__dict__
        # label = info.pop(label_key, None)
        info['name'] = info[
            label_key]  # property with name 'name' is important for displaying (as a label on node) purpose
        del info[label_key]

        flatten_info_dict = get_flattened_dictionary(info)

        node_data = {}
        node_data["id_key"] = id_key
        node_data["node_type"] = node_type
        node_data["node_properties_dict"] = flatten_info_dict
        nodes_data.append(node_data)

    return nodes_data




def server_command_initiator(server_ip, private_key_path, vm_username):
    """

    :param server_ip:
    :param private_key_path:
    :param vm_username:
    :return:
    """
    if not os.path.exists(private_key_path):
        raise Exception("Exception occured: Private key files path not found.")

    command = "sudo docker ps --format \"{{json .}}\""
    ssh_cmd_executor = ShellCommandExecutor()
    ssh_cmd_executor.connect(ip=server_ip, username=vm_username, private_key_file_path=private_key_path)

    stdin, stdout, stderr = ssh_cmd_executor.execute_command(command)
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
        ssh_cmd_executor.close_connection()
    except:
        pass
    return containers_list

def create_containers_nodes(node_type, server_name_attr, private_keys_folder, nova_querier,
                            vm_username):
    search_opts = {'all_tenants': 1}
    for s in fetch_servers(search_opts):  # todo: get servers from db instead of openstack
        server_id = s.node_attributes.__dict__["id"]
        server = nova_querier.get_server(server_id)

        ip = server.addresses[list(server.addresses.keys())[0]][1]["addr"]
        private_key_path = os.path.join(private_keys_folder, server.user_id)

        containers_list = server_command_initiator(server_ip=ip, private_key_path=private_key_path, vm_username=vm_username)
        for container in containers_list:
            container["server_name"] = s.node_attributes.__dict__[server_name_attr]
            container["server_id"] = server_id

        nodes = prepare_node_data(data_list=containers_list, node_type=node_type, id_key="id")
        return nodes
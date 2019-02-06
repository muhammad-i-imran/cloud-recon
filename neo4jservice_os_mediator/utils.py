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

        return node_data


###TODO: later move it somewhere else
def create_containers_nodes(node_type, server_name_attr, private_keys_folder, nova_querier,
                            vm_username):

    import json
    try:
        from openstackqueryapi.queryos import ShellCommandExecutor
    except Exception as ex:
        print("Exception occurred: " + str(ex))
    import os

    ssh_cmd_executor = ShellCommandExecutor()
    # if not cloud_config_info["SERVERS"]["data"]:
    #     return
    command = "sudo docker ps --format \"{{json .}}\""

    for s in nova_querier.get_servers():  # todo: get all servers using generator (yield)
        server_id = s.node_attributes.__dict__["id"]
        server = nova_querier.get_server(server_id)

        ip = server.addresses[list(server.addresses.keys())[0]][1]["addr"]
        private_key_path = os.path.join(private_keys_folder, server.user_id)
        if not os.path.exists(private_key_path):
            continue
        ssh_cmd_executor.connect(ip=ip, username=vm_username, private_key_file_path=private_key_path)

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

            container_info_dict["server_name"] = s.node_attributes.__dict__[server_name_attr]
            container_info_dict["server_id"] = server_id
            containers_list.append(container_info_dict)
        nodes = prepare_node_data(data_list=containers_list, node_type=node_type, id_key="id")
        try:
            ssh_cmd_executor.close_connection()
        except:
            pass
        return nodes
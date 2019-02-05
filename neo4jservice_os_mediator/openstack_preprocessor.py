import re

from graphelementsdispatcher.node_manager import *
from graphelementsdispatcher.relationship_manager import *
from osquerieshandler.osqueriers import *
from utils import *

"""This file contains functionality specific to OpenStack"""


def prepare_node_data(data_list, node_type, label_key='name', id_key="id"):
    nodes = []
    for i in data_list:
        info = i if type(i) is dict else i.__dict__
        # label = info.pop(label_key, None)
        info['name'] = info[
            label_key]  # property with name 'name' is important for displaying (as a label on node) purpose
        del info[label_key]

        flatten_info_dict = get_flattened_dictionary(info)
        node = NodeManager.create_node(id_key, node_type, flatten_info_dict)
        nodes.append(node)
    return nodes


def create_containers_nodes(node_type, server_name_attr, cloud_config_info, private_keys_folder, nova_querier,
                            vm_username):
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


def create_servers(node_type):
    prepare_node_data(data_list=novaQuerier.getServers(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_containers(node_type):
    create_containers_nodes(node_type=node_type,
                            server_name_attr=cloud_config_info["SERVERS"][
                                "name_attr"],
                            cloud_config_info=cloud_config_info,
                            private_keys_folder=PRIVATE_KEYS_FOLDER,
                            nova_querier=novaQuerier,
                            vm_username=VM_USERNAME)


def create_host_aggregates(node_type):
    prepare_node_data(data_list=novaQuerier.getHostAggregates(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_availability_zones(node_type):
    prepare_node_data(data_list=novaQuerier.getAvailabilityZones(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_services(node_type):
    prepare_node_data(data_list=novaQuerier.getServices(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_hypervisors(node_type):
    prepare_node_data(data_list=novaQuerier.getHypervisors(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_flavors(node_type):
    prepare_node_data(data_list=novaQuerier.getFlavors(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_volumes(node_type):
    prepare_node_data(data_list=cinderQuerier.getVolumes(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_key_pairs(node_type):
    prepare_node_data(data_list=novaQuerier.getKeyPairs(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_images(node_type):
    prepare_node_data(data_list=glanceQuerier.getImages(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_networks(node_type):
    prepare_node_data(data_list=neutronQuerier.getNetworks(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_subnets(node_type):
    prepare_node_data(data_list=neutronQuerier.getSubNets(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_routers(node_type):
    prepare_node_data(data_list=neutronQuerier.getRouters(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def create_users(node_type):
    prepare_node_data(data_list=keystoneQuerier.getUsers(),
                      node_type=node_type,
                      label_key=cloud_config_info[node_type]["name_attr"],
                      id_key=cloud_config_info[node_type]["id_key"])


def not_supported():
    raise Exception("Not supported yet.")


def create_graph_elements(element_type, prefix_string):
    switcher = {
        prefix_string + "SERVERS": create_servers,
        prefix_string + "HOST_AGGREGATES": create_host_aggregates,
        prefix_string + "AVAILABILITY_ZONES": create_availability_zones,
        prefix_string + "SERVICES": create_services,
        prefix_string + "HYPERVISORS": create_hypervisors,
        prefix_string + "FLAVORS": create_flavors,
        prefix_string + "VOLUMES": create_volumes,
        prefix_string + "KEY_PAIRS": create_key_pairs,
        prefix_string + "IMAGES": create_images,
        prefix_string + "NETWORKS": create_networks,
        prefix_string + "SUBNETS": create_subnets,
        prefix_string + "ROUTERS": create_routers,
        prefix_string + "CONTAINERS": create_containers,
        prefix_string + "USERS": create_users
    }
    func = switcher.get(element_type, lambda: not_supported)
    return func


def begin_node_create(cloud_config_info, prefix_string=""):
    nodes = list(cloud_config_info.keys())
    nodes.remove(prefix_string + "CONTAINERS")

    for node_type in nodes:
        try:
            create_graph_elements(node_type, prefix_string)(node_type)
        except Exception as ex:
            print("".join(["Exception occured: ", str(ex)]))

    # for container (because it depends on SERVERS)
    try:
        create_graph_elements(prefix_string + "CONTAINERS", prefix_string)(prefix_string + "CONTAINERS")
    except Exception as e:
        print("Exception occured: " + str(e))
        pass


def begin_relationship_create(cloud_config_info):
    for key in cloud_config_info:
        source_node_type = key
        relationship_infos = cloud_config_info[key]["RELATIONSHIPS"]
        for relationship_info in relationship_infos:
            source_property_name = relationship_info["source_property_name"]
            target_node_type = relationship_info["target_node_type"]
            target_property_name = relationship_info["target_property_name"]
            relationship_name = relationship_info["relationship_name"]
            relationship_properties = relationship_info["relationship_properties"]
            is_source_attr_name_regex = relationship_info["is_source_attr_name_regex"]  # todo: get rid of regexes

            ##todo: fetch data directly for this key from openstack
            data = list()

            for d in data:
                target_node_properties = {target_property_name: d[target_property_name]}
                if is_source_attr_name_regex:
                    source_property_names = list(filter(re.compile(source_property_name).match,
                                                        d.node_attributes.__dict__.keys()))

                    for property_name in source_property_names:
                        source_node_properties = {property_name: d[property_name]}

                        data = {}
                        data["source_node_type"] = source_node_type
                        data["source_node_properties"] = source_node_properties
                        data["target_node_type"] = target_node_type
                        data["target_node_properties"] = target_node_properties
                        data["relationship"] = relationship_name
                        data["relationship_properties"] = relationship_properties

                        RelationshipManager.create_relationship(data)
                else:
                    source_node_properties = {source_property_name: d[source_property_name]}
                    data = {}
                    data["source_node_type"] = source_node_type
                    data["source_node_properties"] = source_node_properties
                    data["target_node_type"] = target_node_type
                    data["target_node_properties"] = target_node_properties
                    data["relationship"] = relationship_name
                    data["relationship_properties"] = relationship_properties

                    RelationshipManager.create_relationship(data)

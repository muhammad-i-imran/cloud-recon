from osquerieshandler.osqueriers import *
from utils import *

"""
Convention of the function naming is very important here. 
The convention is: 
 create_<config json key>()
 
 
 e.g.,
 
 for configuration
 {
 "SERVERS": ...
 }
 
 the corresponding function will be: create_servers()
"""

def create_servers(node_type, label_key, id_key):
    # TODO: add NodeManager.create_node(data)
    prepare_node_data(data_list=novaQuerier.getServers(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_containers(node_type, server_name_attr, vm_username, private_keys_folder):
    #todo: refactor this function
    create_containers_nodes(node_type=node_type,
                            server_name_attr=server_name_attr,
                            private_keys_folder=private_keys_folder,
                            nova_querier=novaQuerier,
                            vm_username=vm_username)

def create_host_aggregates(node_type, label_key, id_key):
    prepare_node_data(data_list=novaQuerier.getHostAggregates(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_availability_zones(node_type, label_key, id_key):
    prepare_node_data(data_list=novaQuerier.getAvailabilityZones(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_services(node_type, label_key, id_key):
    prepare_node_data(data_list=novaQuerier.getServices(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_hypervisors(node_type, label_key, id_key):
    prepare_node_data(data_list=novaQuerier.getHypervisors(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_flavors(node_type, label_key, id_key):
    prepare_node_data(data_list=novaQuerier.getFlavors(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_volumes(node_type, label_key, id_key):
    prepare_node_data(data_list=cinderQuerier.getVolumes(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_key_pairs(node_type, label_key, id_key):
    prepare_node_data(data_list=novaQuerier.getKeyPairs(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_images(node_type, label_key, id_key):
    prepare_node_data(data_list=glanceQuerier.getImages(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_networks(node_type, label_key, id_key):
    prepare_node_data(data_list=neutronQuerier.getNetworks(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_subnets(node_type, label_key, id_key):
    prepare_node_data(data_list=neutronQuerier.getSubNets(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_routers(node_type, label_key, id_key):
    prepare_node_data(data_list=neutronQuerier.getRouters(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)

def create_users(node_type, label_key, id_key):
    prepare_node_data(data_list=keystoneQuerier.getUsers(),
                      node_type=node_type,
                      label_key=label_key,
                      id_key=id_key)
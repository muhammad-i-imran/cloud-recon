from graphelementsdispatcher.node_manager import NodeManager
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
########################################################################################################################

queriers = QuerierProvider()

########################################################################################################################

def fetch_servers(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    return queriers.nova_querier.getServers(search_opts)


def fetch_containers(node_type, server_name_attr, vm_username, private_keys_folder):
    return ""
    # create_containers_nodes(node_type=node_type,
    #                         server_name_attr=server_name_attr,
    #                         private_keys_folder=private_keys_folder,
    #                         nova_querier=novaQuerier,
    #                         vm_username=vm_username)


def fetch_host_aggregates(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    return queriers.nova_querier.getHostAggregates(search_opts)


def fetch_availability_zones(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.nova_querier.getAvailabilityZones(search_opts)


def fetch_services(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.nova_querier.getServices(search_opts)


def fetch_hypervisors(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.nova_querier.getHypervisors(search_opts)


def fetch_flavors(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.nova_querier.getFlavors(search_opts)


def fetch_volumes(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.cinder_querier.getVolumes(search_opts)


def fetch_key_pairs(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.nova_querier.getKeyPairs(search_opts)


def fetch_images(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.glance_querier.getImages(search_opts)


def fetch_networks(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.neutron_querier.getNetworks(search_opts)


def fetch_subnets(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.neutron_querier.getSubNets(search_opts)


def fetch_routers(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.neutron_querier.getRouters(search_opts)


def fetch_users(search_opts={}):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """

    return queriers.keystone_querier.getUsers(search_opts)


########################################################################################################################

def get_prepared_node(data, node_type, label_key, id_key):
    return prepare_node_data(data_list=data, node_type=node_type, label_key=label_key, id_key=id_key)


########################################################################################################################

def create_servers(node_type, label_key, id_key):
    search_opts = {'all_tenants': 1}
    data = fetch_servers(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_containers(node_type, server_name_attr, vm_username, private_keys_folder):
    # todo: refactor this function
    data = fetch_containers()
    create_containers_nodes(node_type=node_type,
                            server_name_attr=server_name_attr,
                            private_keys_folder=private_keys_folder,
                            nova_querier=novaQuerier,
                            vm_username=vm_username)
    node_data = {}
    NodeManager.create_node(node_data)


def create_host_aggregates(node_type, label_key, id_key):
    data = fetch_host_aggregates()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)

    NodeManager.create_node(node_data)


def create_availability_zones(node_type, label_key, id_key):
    data = fetch_availability_zones()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_services(node_type, label_key, id_key):
    data = fetch_services()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_hypervisors(node_type, label_key, id_key):
    data = fetch_hypervisors()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_flavors(node_type, label_key, id_key):
    data = fetch_flavors()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_volumes(node_type, label_key, id_key):
    data = fetch_volumes()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_key_pairs(node_type, label_key, id_key):
    data = fetch_key_pairs()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_images(node_type, label_key, id_key):
    data = fetch_images()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_networks(node_type, label_key, id_key):
    data = fetch_networks()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_subnets(node_type, label_key, id_key):
    data = fetch_subnets()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_routers(node_type, label_key, id_key):
    data = fetch_routers()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)


def create_users(node_type, label_key, id_key):
    data = fetch_users()
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    NodeManager.create_node(node_data)
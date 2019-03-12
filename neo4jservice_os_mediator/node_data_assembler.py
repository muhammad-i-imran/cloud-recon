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

queriers = OpenStackQueriersProvider()


########################################################################################################################

def fetch_servers(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}
    return queriers.nova_querier.get_servers(search_opts)


def fetch_containers(node_type, search_opts=None):
    """

    :param node_type:
    :param server_name_attr:
    :param vm_username:
    :param private_keys_folder:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    return fetch_and_prepare_container_nodes(node_type)


def fetch_host_aggregates(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}
    return queriers.nova_querier.get_host_aggregates(search_opts)


def fetch_availability_zones(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.nova_querier.get_availability_zones(search_opts)


def fetch_services(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.nova_querier.get_services(search_opts)


def fetch_hypervisors(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.nova_querier.get_hypervisors(search_opts)


def fetch_flavors(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.nova_querier.get_flavors(search_opts)


def fetch_volumes(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.cinder_querier.get_volumes(search_opts)


def fetch_key_pairs(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.nova_querier.get_key_pairs(search_opts)


def fetch_images(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.glance_querier.get_images(search_opts)


def fetch_networks(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.neutron_querier.get_networks(search_opts)


def fetch_subnets(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.neutron_querier.get_subnets(search_opts)


def fetch_routers(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.neutron_querier.get_routers(search_opts)


def fetch_users(search_opts=None):
    """

    :param search_opts: (dict) filter options can be provided in search_opts
    :return:
    """
    if search_opts is None:
        search_opts = {}

    return queriers.keystone_querier.get_users(search_opts)


########################################################################################################################

def get_prepared_node(data, node_type, label_key, id_key):
    return prepare_node_data(data_list=data, node_type=node_type, label_key=label_key, id_key=id_key)


########################################################################################################################

def create_servers(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    search_opts['all_tenants'] = 1  # todo: may be take this option as configuration from user.
    data = fetch_servers(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_containers(node_type, label_key="name", id_key="id", search_opts=None):
    """

    :param node_type:
    :param server_name_attr:
    :param vm_username:
    :param private_keys_folder:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_containers(node_type, search_opts=search_opts)
    node_data = get_prepared_node(data=data, node_type=node_type, label_key=label_key, id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_host_aggregates(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_host_aggregates(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)

    for d in node_data:
        NodeManager.create_node(d)


def create_availability_zones(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_availability_zones(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_services(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_services(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_hypervisors(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_hypervisors(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_flavors(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_flavors(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_volumes(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_volumes(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_key_pairs(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_key_pairs(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_images(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_images(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_networks(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_networks(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_subnets(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_subnets(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_routers(node_type, label_key, id_key, search_opts=None):
    """

    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_routers(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)


def create_users(node_type, label_key, id_key, search_opts=None):
    """
    
    :param node_type:
    :param label_key:
    :param id_key:
    :return:
    """
    if search_opts is None:
        search_opts = {}
    data = fetch_users(search_opts)
    node_data = get_prepared_node(data=data,
                                  node_type=node_type,
                                  label_key=label_key,
                                  id_key=id_key)
    for d in node_data:
        NodeManager.create_node(d)

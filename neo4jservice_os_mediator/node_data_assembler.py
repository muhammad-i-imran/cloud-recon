from graphelementsdispatcher.node_manager import NodeManager
from osquerieshandler.osqueriers import *
from utils import *

from logging_config import Logger


########################################################################################################################

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger
########################################################################################################################

class OpenStackDataFecher(object):

    def __init__(self, queriers):
        self.queriers = queriers

    def fetch_servers(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching servers.")
        if search_opts is None:
            search_opts = {}
        return self.queriers.nova_querier.get_servers(search_opts)

    def fetch_host_aggregates(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching host aggregates.")
        if search_opts is None:
            search_opts = {}
        return self.queriers.nova_querier.get_host_aggregates(search_opts)


    def fetch_availability_zones(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching availability zones.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.nova_querier.get_availability_zones(search_opts)


    def fetch_services(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching services.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.nova_querier.get_services(search_opts)


    def fetch_hypervisors(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching hypervisors.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.nova_querier.get_hypervisors(search_opts)


    def fetch_flavors(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching flavors.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.nova_querier.get_flavors(search_opts)


    def fetch_volumes(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching volumes.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.cinder_querier.get_volumes(search_opts)


    def fetch_key_pairs(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching key pairs.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.nova_querier.get_key_pairs(search_opts)


    def fetch_images(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching images.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.glance_querier.get_images(search_opts)


    def fetch_networks(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching networks.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.neutron_querier.get_networks(search_opts)


    def fetch_subnets(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching subnets.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.neutron_querier.get_subnets(search_opts)


    def fetch_routers(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching routers.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.neutron_querier.get_routers(search_opts)


    def fetch_users(self, search_opts=None):
        """

        :param search_opts: (dict) filter options can be provided in search_opts
        :return:
        """
        logger.debug("Fetching users.")
        if search_opts is None:
            search_opts = {}

        return self.queriers.keystone_querier.get_users(search_opts)


########################################################################################################################

def get_prepared_node(data, node_type, node_secondary_labels, label_key, id_key):
    return prepare_node_data(data_list=data, node_type=node_type, node_secondary_labels=node_secondary_labels,
                             label_key=label_key, id_key=id_key)


########################################################################################################################

class NodeCreator(object):
    def __init__(self):
        queriers = OpenStackQueriersProvider()
        self.fetcher = OpenStackDataFecher(queriers)

    def _init_nodes_creation(self, node_data):
        for d in node_data:
            NodeManager.create_node(d)

    def create_servers(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        search_opts['all_tenants'] = 1  # todo: may be take this option as configuration from user.
        data = self.fetcher.fetch_servers(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_containers(self, node_type, node_secondary_labels, label_key="name", id_key="id", data=None):
        """

        :param node_type:
        :param server_name_attr:
        :param vm_username:
        :param private_keys_folder:
        :return:
        """
        if data is None:
            data = {}
        data_list = []
        if type(data) is dict:
            data_list.append(data)
        node_data = get_prepared_node(data=data_list, node_type=node_type, node_secondary_labels=node_secondary_labels,
                                      label_key=label_key, id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_host_aggregates(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_host_aggregates(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_availability_zones(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_availability_zones(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_services(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_services(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_hypervisors(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_hypervisors(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_flavors(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_flavors(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_volumes(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_volumes(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_key_pairs(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_key_pairs(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_images(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_images(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_networks(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_networks(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_subnets(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_subnets(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_routers(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_routers(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

    def create_users(self, node_type, node_secondary_labels, label_key, id_key, search_opts=None):
        """

        :param node_type:
        :param label_key:
        :param id_key:
        :return:
        """
        if search_opts is None:
            search_opts = {}
        data = self.fetcher.fetch_users(search_opts)
        node_data = get_prepared_node(data=data,
                                      node_type=node_type,
                                      node_secondary_labels=node_secondary_labels,
                                      label_key=label_key,
                                      id_key=id_key)
        self._init_nodes_creation(node_data)

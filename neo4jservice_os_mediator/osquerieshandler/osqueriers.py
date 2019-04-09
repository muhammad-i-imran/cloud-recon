from cloudconnectionshandler.cloud_connections_manager import CloudConnectionProviderFactory
from envvars import *
from openstackqueryapi.queryos import *
import envvars
from logging_config import Logger

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

"""
It is OpenStack-specific implementation... so far
"""

cloud_type = CLOUD_TYPE.lower()


class OpenStackQueriersProvider(object):
    cloud_connection_provider_factory_instance = CloudConnectionProviderFactory()
    cloud_connection_provider = cloud_connection_provider_factory_instance.get_cloud_connection(cloud_type=cloud_type,
                                                                                                auth_url=OS_AUTH_URL,
                                                                                                username=OS_USERNAME,
                                                                                                password=OS_PASSWORD,
                                                                                                project_name=OS_PROJECT_NAME,
                                                                                                os_user_domain_name=OS_USER_DOMAIN_NAME,
                                                                                                os_project_domain_id=OS_PROJECT_DOMAIN_ID,
                                                                                                api_version=OS_API_VERSION)

    def __init__(self):
        connection = OpenStackQueriersProvider.cloud_connection_provider.get_connection()
        self.nova_querier = NovaQuerier(connection)
        self.neutron_querier = NeutronQuerier(connection)
        self.cinder_querier = CinderQuerier(connection)
        self.keystone_querier = KeystoneQuerier(connection)
        self.glance_querier = GlanceQuerier(connection)

        logger.debug("Getting connection for nova.")
        self.nova_querier.connect()

        logger.debug("Getting connection for neutron.")
        self.neutron_querier.connect()

        logger.debug("Getting connection for cinder.")
        self.cinder_querier.connect()

        logger.debug("Getting connection for keystone.")
        self.keystone_querier.connect()

        logger.debug("Getting connection for glance.")
        self.glance_querier.connect()

    # @classmethod
    # def get_connector(cls, cloud_type, element_key):
    #     return mapping[cloud_type][element_key]
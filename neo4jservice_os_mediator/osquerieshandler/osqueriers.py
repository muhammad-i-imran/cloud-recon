from envvars import *
from cloudconnectionshandler.cloud_connections_manager import CloudConnectionProviderFactory

"""
It is OpenStack-specific implementation... so far
"""

try:
    from openstackqueryapi.queryos import *
except ImportError as e:
    pass

cloud_type = "openstack" # todo: read from env
cloud_connection_provider_factory_instance = CloudConnectionProviderFactory()
cloud_connection_provider = cloud_connection_provider_factory_instance.get_cloud_connection(cloud_type=cloud_type, auth_url=OS_AUTH_URL, username=OS_USERNAME,
                                               password=OS_PASSWORD,
                                               project_name=OS_PROJECT_NAME,
                                               os_user_domain_name=OS_USER_DOMAIN_NAME,
                                               os_project_domain_id=OS_PROJECT_DOMAIN_ID,
                                               api_version=OS_API_VERSION)
#TODO: refactor the following
connection = cloud_connection_provider.get_connection()
novaQuerier = NovaQuerier(connection)
neutronQuerier = NeutronQuerier(connection).connect()
cinderQuerier = CinderQuerier(connection).connect()
keystoneQuerier = KeystoneQuerier(connection).connect()
glanceQuerier = GlanceQuerier(connection).connect()

novaQuerier.connect()
neutronQuerier.connect()
cinderQuerier.connect()
keystoneQuerier.connect()
glanceQuerier.connect()
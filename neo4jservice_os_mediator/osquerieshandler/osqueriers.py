from envvars import *
from cloudconnectionshandler.cloud_connections_manager import CloudConnectionProviderFactory

"""
It is OpenStack-specific implementation... so far
"""

try:
    from openstackqueryapi.queryos import *
except ImportError as e:
    pass

cloud_type = CLOUD_TYPE.lower()
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
neutronQuerier = NeutronQuerier(connection)
cinderQuerier = CinderQuerier(connection)
keystoneQuerier = KeystoneQuerier(connection)
glanceQuerier = GlanceQuerier(connection)

novaQuerier.connect()
neutronQuerier.connect()
cinderQuerier.connect()
keystoneQuerier.connect()
glanceQuerier.connect()



mapping = {
    "openstack": {
        "SERVERS": novaQuerier,
        "NETWORKS":neutronQuerier,
        "SUBNETS":neutronQuerier,
        "ROUTERS": neutronQuerier,
        "VOLUME": cinderQuerier,
        "USERS": keystoneQuerier,
        "IMAGES" : glanceQuerier
    }
}

def get_connector(cloud_type, element_key):
    return mapping[cloud_type][element_key]
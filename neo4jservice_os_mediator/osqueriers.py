from openstackqueryapi.queryos import *
from envvars import *


def getOpenstackConnection(auth_url, username, password, project_name, os_user_domain_name, os_project_domain_id,
                           api_version):
    return OpenstackConnector(auth_url=auth_url, username=username, password=password, project_name=project_name,
                              os_user_domain_name=os_user_domain_name, os_project_domain_id=os_project_domain_id,
                              api_version=api_version)


conn = getOpenstackConnection(auth_url=OS_AUTH_URL, username=OS_USERNAME, password=OS_PASSWORD,
                              project_name=OS_PROJECT_NAME,
                              os_user_domain_name=OS_USER_DOMAIN_NAME, os_project_domain_id=OS_PROJECT_DOMAIN_ID,
                              api_version=OS_API_VERSION)

novaQuerier = NovaQuerier(conn)
novaQuerier.connect()

glanceQuerier = GlanceQuerier(conn)
glanceQuerier.connect()

neutronQuerier = NeutronQuerier(conn)
neutronQuerier.connect()

cinderQuerier = CinderQuerier(conn)
cinderQuerier.connect()

keystoneQuerier = KeystoneQuerier(conn)
keystoneQuerier.connect()
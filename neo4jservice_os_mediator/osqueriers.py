from openstackqueryapi.queryos import *
from envvars import *

def getOpenstackConnection(auth_url, username, password, project_id, version):
    return OpenstackConnector(auth_url=auth_url, username=username, password=password, project_id=project_id,
                              version=version)

conn = getOpenstackConnection(auth_url=OS_AUTH_URL, username=OS_USERNAME, password=OS_PASSWORD,
                              project_id=OS_PROJECT_ID, version=OS_API_VERSION)


novaQuerier = NovaQuerier(conn)
novaQuerier.connect()

glanceQuerier = GlanceQuerier(conn)
glanceQuerier.connect()

neutronQuerier = NeutronQuerier(conn)
neutronQuerier.connect()

cinderQuerier = CinderQuerier(conn)
cinderQuerier.connect()
import os

NEO4J_SERVICE_URL = os.getenv('NEO4J_SERVICE_URL1', 'http://x.x.x.x:15135/neo4j')
OS_AUTH_URL = os.getenv('OS_AUTH_URL', "http://x.x.x.x:5000/v3")
OS_USERNAME = os.getenv('OS_USERNAME', "xxxxxx")
OS_PASSWORD = os.getenv('OS_PASSWORD', "xxxxxxxx")
OS_PROJECT_NAME = os.getenv('OS_PROJECT_NAME', "xxxxxx_project")
OS_USER_DOMAIN_NAME=os.getenv('OS_USER_DOMAIN_NAME', 'Default')
OS_PROJECT_DOMAIN_ID=os.getenv('OS_PROJECT_DOMAIN_ID', 'default')
OS_API_VERSION = os.getenv('OS_API_VERSION', "2")
CONFIG_FILE_PATH = os.getenv('CONFIG_FILE_PATH1', '/openstack_info.json')
NOTIFICATION_TRANSPORT_URL = os.getenv('NOTIFICATION_TRANSPORT_URL', "rabbit://xxxxxxxxxxx:xxxxxxx@x.x.x.x:5672")
NOTIFICATION_EVENT_TYPE = os.getenv('NOTIFICATION_EVENT_TYPE', "^(compute.instance|network).(create|delete).end$")
NOTIFICATION_PUBLISHER_ID = os.getenv('NOTIFICATION_PUBLISHER_ID', "^.*")
OPENSTACK_NOTIFICATION_TOPIC_NAME = os.getenv('OPENSTACK_NOTIFICATION_TOPIC_NAME', "notifications")
OPENSTACK_NOTIFICATION_EXCHANGE_NAME = os.getenv('OPENSTACK_NOTIFICATION_EXCHANGE_NAME', "openstack")
DOCKER_NOTIFICATION_EXCHANGE_NAME = os.getenv('DOCKER_NOTIFICATION_EXCHANGE_NAME', "docker")
DOCKER_NOTIFICATION_TOPIC_NAME = os.getenv('OPENSTACK_NOTIFICATION_TOPIC_NAME', "docker_notifications")
PRIVATE_KEYS_FOLDER = os.getenv('PRIVATE_KEYS_FOLDER', "/keys")
VM_USERNAME = os.getenv('VM_USERNAME', "xxxx")
TIME_TO_WAIT = os.getenv("TIME_TO_WAIT", '1000')
GRAPH_ELEMENT_TYPE_PREFIX = os.getenv("GRAPH_ELEMENT_TYPE_PREFIX","xxxx")
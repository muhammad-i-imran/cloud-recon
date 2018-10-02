from keystoneauth1 import loading
from keystoneauth1 import session
import novaclient
from novaclient import client
import neutronclient
from neutronclient.v2_0.client import Client

import glanceclient
import cinderclient
from cinderclient.v2 import Client
import manilaclient
from manilaclient.v2 import client
from manilaclient.client import Client
import ironicclient
from ironicclient.v1 import client
import swiftclient
from swiftclient.client import Connection
import paramiko
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import subprocess


class OpenstackConnector(object):
    def __init__(self, auth_url, username, password, project_id, version):
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.project_id = project_id
        self.version = version


class NovaQuerier(object):
    def __init__(self, os_connector):
        self.nova = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self.os_connector.auth_url,
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.nova = novaclient.client.Client(self.os_connector.version, session=sess)

    def getFlavors(self):
        flavors_list = self.nova.flavors.list()
        return flavors_list

    def getHostAggregates(self):
        host_aggregates_list = self.nova.aggregates.list()
        return host_aggregates_list

    def getServices(self):
        services_list = self.nova.services.list()
        return services_list

    def getHypervisors(self):
        hypervisors_list = self.nova.hypervisors.list()
        return hypervisors_list

    def getServers(self):
        servers_list = self.nova.servers.list()
        return servers_list

    def getAvailabilityZones(self):
        availability_zones = self.nova.availability_zones.list()
        return availability_zones

    def getKeyPairs(self):
        keypairs_list = self.nova.keypairs.list()
        return keypairs_list

    def getServer(self, id):
        return self.nova.servers.get(id)

    def execCommandWithSsh(self, command):
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)


class NeutronQuerier(object):
    def __init__(self, os_connector):
        self.neutron = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self.os_connector.auth_url,
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.neutron = neutronclient.v2_0.client.Client(session=sess)

    def getNetworks(self):
        networks = self.neutron.list_networks()["networks"]
        return networks

    # ...
    def getSubNets(self):
        subnets = self.neutron.list_subnets()["subnets"]
        return subnets

    def getRouters(self):
        routers = self.neutron.list_routers()["routers"]
        return routers


class GlanceQuerier(object):
    def __init__(self, os_connector):
        self.glance = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self.os_connector.auth_url,
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.glance = glanceclient.Client('1', session=sess)

    def getImages(self):
        images_list = self.glance.images.list()
        return images_list

    def getImageMembers(self, image_id):
        image_members_list = self.glance.image_members.list(image_id)
        return image_members_list


class CinderQuerier(object):
    def __init__(self, os_connector):
        self.cinder = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self.os_connector.auth_url,
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.cinder = cinderclient.v2.Client(session=sess)

    def getVolumes(self):
        volumes_list = self.cinder.volumes.list()
        return volumes_list


class ManilaQuerier(object):
    def __init__(self, os_connector):
        self.manila = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url='http://130.149.249.252:5000/',
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.manila = manilaclient.v2.client.Client('2', session=sess)


class IronicQuerier(object):
    def __init__(self, os_connector):
        self.ironic = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self.os_connector.auth_url,
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.ironic = ironicclient.v1.client.Client('1', session=sess)


class SwiftQuerier(object):
    def __init__(self, os_connector):
        self.swift = None
        self.os_connector = os_connector

    def connect(self):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self.os_connector.auth_url,
                                        username=self.os_connector.username,
                                        password=self.os_connector.password,
                                        project_id=self.os_connector.project_id)
        sess = session.Session(auth=auth)
        self.swift = swiftclient.client.Connection(session=sess)


class CustomVirtualMachineQuerier(object):
    def __init__(self):
        self.ssh = None

    def connect(self, ip, username, private_key_file_path):
        key = paramiko.RSAKey.from_private_key_file(private_key_file_path)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip, username=username, pkey=key)

    def executeCommandOnVM(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdin, stdout, stderr

    def closeConnection(self):
        self.ssh.close()
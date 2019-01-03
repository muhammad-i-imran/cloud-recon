import abc

try:
    from openstackqueryapi.queryos import *  ## depends on the cloud type...
except ImportError as e:
    pass


class CloudConnectionProvider(metaclass=abc.ABCMeta):
    CLOUD_TYPE = None

    def __init__(self, auth_url, username, password, project_name, os_user_domain_name, os_project_domain_id,
                 api_version):  # todo: reduce number of parameters
        # only the shared parameters should be here
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.project_name = project_name
        self.os_user_domain_name = os_user_domain_name
        self.os_project_domain_id = os_project_domain_id
        self.api_version = api_version

    @abc.abstractmethod
    def get_connection(self):
        pass

    @classmethod
    def check_cloud_type(cls, cloud_type):
        return cls.CLOUD_TYPE == cloud_type


class OpenStackCloudConnectionProvider(CloudConnectionProvider):
    CLOUD_TYPE = "openstack"

    def __init__(self):
        CloudConnectionProvider.__init__(self)

    def get_connection(self):
        self.connection = OpenstackConnector(auth_url=self.auth_url, username=self.username, password=self.password,
                                             project_name=self.project_name,
                                             os_user_domain_name=self.os_user_domain_name,
                                             os_project_domain_id=self.os_project_domain_id,
                                             api_version=self.api_version)
        return self.connection


class AWSCloudConnectionProvider(CloudConnectionProvider):
    CLOUD_TYPE = "aws"

    def __init__(self):
        CloudConnectionProvider.__init__(self)
        raise NotImplementedError("Functionalirt for AWS is not yet implemented.")

    def get_connection(self):
        raise NotImplementedError("Functionality for AWS is not yet implemented.")


class CloudConnectionProviderFactory(object):
    SUPPORTED_CLOUD_CONNECTION_PROVIDERS = [OpenStackCloudConnectionProvider]

    def __init__(self):
        pass

    def get_cloud_connection(self, cloud_type, **parameters):
        for cloud_connection_provider in self.SUPPORTED_CLOUD_CONNECTION_PROVIDERS:
            if cloud_connection_provider.check_cloud_type(cloud_type):
                return cloud_connection_provider(parameters)
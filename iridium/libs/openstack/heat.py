__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from iridium.libs.openstack import keystone
from heatclient import client


class HeatBase(object):
    def __init__(self, version):
        creds = keystone.create_keystone()
        tenant_id = creds.tenants.id
        heat_url = creds.auth_url + tenant_id
        auth_token = creds.auth_token
        self.heat_session = client.Client(version, endpoint=heat_url, token=auth_token)

    def stack_list(self):
        pass

    def stack_create(self):
        pass

    def stack_delete(self):
        pass

    def stack_show(self):
        pass

    def stack_update(self):
        pass

    def resource_list(self):
        pass

    def resource_create(self):
        pass

    def config_create(self):
        pass

    def config_delete(self):
        pass

    def config_show(self):
        pass

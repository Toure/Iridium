__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from iridium.libs.openstack import keystone
from heatclient.client import Client as hc


class HeatBase(object):
    def __init__(self, version):
        ks = keystone.create_keystone()
        heat_url = ks.auth_url + '/%s' % ks.tenant_id
        self.heat_session_obj = hc(version, endpoint=heat_url, token=ks.auth_token)

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

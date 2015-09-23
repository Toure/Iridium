__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from iridium.libs.openstack import keystone
from ironicclient import client


class IronicBase(object):
    def __init__(self, version=1):
        creds = keystone.keystone_retrieve(version='v2')
        ironic_kwargs = {'os_' + k: v for k, v in creds}
        self.ironic_session = client.get_client(version, **ironic_kwargs)

    def chassis_create(self, name, count):
        pass

    def chassis_delete(self, name):
        pass

    def node_create(self, name, count):
        pass

    def node_delete(self, name):
        pass

    def driver_info(self):
        pass

    def port_create(self, name, count):
        pass

    def port_delete(self, name):
        pass

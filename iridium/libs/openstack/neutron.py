__author__ = "Toure Dunnon, Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com, stoner@redhat.com"
__status__ = "Alpha"

from neutronclient.v2_0.client import Client
from iridium.libs.openstack import keystone
from iridium.plugins.inspector import Plugin

class NeutronBase(object):
    def __init__(self):
        creds = keystone.keystone_retrieve()
        self.neutron_session = Client(**creds)

    def __getattr__(self, item):
        """
        getattr is responsible for searching requested methods which exist in the
        plugin tree.
        :param item: name of method
        :return: remote method.
        """
        __plugin = Plugin()
        __ext = __plugin.activate_plugins('neutron')
        return getattr(__ext.Common(self.neutron_session), item)

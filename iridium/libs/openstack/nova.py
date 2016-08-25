__author__ = 'toure'


from iridium.plugins.inspector import Plugin
from novaclient import client as nova_client
from iridium.libs.openstack.keystone import KeystoneBase


class NovaBase(KeystoneBase):
    """
    This class is serving as a common interface for both local plugins as well as
    openstack client methods.
    """
    def __init__(self, version='2'):
        super().__init__()
        self.nova_session = nova_client.Client(version, self.keystone_obj)

    def __getattr__(self, item):
        """
        getattr is responsible for searching requested methods which exist in the
        plugin tree.
        :param item: name of method
        :return: remote method.
        """
        __plugin = Plugin()
        __ext = __plugin.activate_plugins('nova')
        return getattr(__ext.Common(self.nova_session), item)

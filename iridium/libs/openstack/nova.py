__author__ = 'toure'


from iridium.plugins.inspector import Plugin
import novaclient.client as nvclient
from iridium.libs.openstack import keystone


class NovaBase(object):
    """
    This class is serving as a common interface for both local plugins as well as
    openstack client methods.
    """
    def __init__(self, version='2'):
        creds = keystone.keystone_retrieve(version='v2')
        nova_cred_list = [creds[key] for key in ["username", "password", "tenant_name", "auth_url"]]
        self.nova_session = nvclient.Client(version, *nova_cred_list)

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

_localhost_author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from iridium.libs.openstack import keystone
from ironicclient import client
from iridium.plugins.inspector import Plugin


class IronicBase(object):
    def __init__(self, version: int = 1) -> object:
        creds = keystone.keystone_retrieve(version='v2')
        ironic_kwargs = {'os_' + k: v for k, v in creds.items()}
        self.ironic_session = client.get_client(version, **ironic_kwargs)

    def __getattr__(self, item):
        """
        getattr is responsible for searching requested methods which exist in the
        plugin tree.
        :param item: name of method
        :return: remote method.
        """
        __plugin = Plugin()
        __ext = __plugin.activate_plugins('ironic')
        return getattr(__ext.Common(self.ironic_session), item)

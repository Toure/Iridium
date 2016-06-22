__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from iridium.libs.openstack import keystone
from heatclient.client import Client as hc
from iridium.plugins.inspector import Plugin


class HeatBase(object):
    def __init__(self, version: int) -> object:
        """

        :type version: int
        """
        ks = keystone.create_keystone()
        heat_url = ks.auth_url + '/%s' % ks.tenant_id
        self.heat_session_obj = hc(version, endpoint=heat_url, token=ks.auth_token)

    def __getattr__(self, item):
        """
        getattr is responsible for searching requested methods which exist in the
        plugin tree.
        :param item: name of method
        :return: remote method.
        """
        __plugin = Plugin()
        __ext = __plugin.activate_plugins('heat')
        return getattr(__ext.Common(self.heat_session), item)

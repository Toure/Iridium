__author__ = 'toure'


from iridium.plugins.inspector import Plugin
import novaclient.client as nvclient
from iridium.libs.openstack import keystone


class NovaBase(object):
    def __init__(self, version='2'):
        creds = keystone.keystone_retrieve(version='v2')
        nova_cred_list = [creds[key] for key in ["username", "password", "tenant_name", "auth_url"]]
        self.nova_session = nvclient.Client(version, *nova_cred_list)
        plugin = Plugin()
        self.extensions = plugin.activate_plugins('nova')



# @six.add_metaclass(abc.ABCMeta)
# class NovaPluginBase(object):

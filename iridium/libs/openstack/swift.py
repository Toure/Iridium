from swiftclient import client as sc
from iridium.libs.openstack import keystone
from iridium.plugins.inspector import Plugin


class SwiftBase(object):
    def __init__(self):
        self.ks = keystone.create_keystone()
        self.storage_location = sc.Connection(authurl=self.ks.auth_url,
                                              user=self.ks.username,
                                              key=self.ks.password,
                                              tenant_name=self.ks.tenant_name,
                                              auth_version='2.0').get_auth()[0]
        plugin = Plugin()
        self.extension = plugin.activate_plugins('swift')



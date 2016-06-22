from swiftclient import client
from iridium.libs.openstack import keystone
from iridium.plugins.inspector import Plugin


class SwiftBase(object):
    def __init__(self):
        self.ks = keystone.create_keystone()
        self.swift_session = client.Connection(authurl=self.ks.auth_url,
                                              user=self.ks.username,
                                              key=self.ks.password,
                                              tenant_name=self.ks.tenant_name,
                                              auth_version='2.0').get_auth()[0]

    def __getattr__(self, item):
        """
        getattr is responsible for searching requested methods which exist in the
        plugin tree.
        :param item: name of method
        :return: remote method.
        """
        __plugin = Plugin()
        __ext = __plugin.activate_plugins('swift')
        return getattr(__ext.Common(self.swift_session), item)

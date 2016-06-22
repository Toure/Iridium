from iridium.plugins.inspector import Plugin


class Common(Plugin):
    def __init__(self, keystone_session):
        self.keystone_session = keystone_session

    def list_tenants(self):
        pass

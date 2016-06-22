from iridium.plugins import Plugin


class Common(Plugin):
    def __init__(self, ironic_session):
        self.ironic_session = ironic_session

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
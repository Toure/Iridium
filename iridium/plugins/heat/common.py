from iridium.plugins import Plugin


class Common(Plugin):
    def __init__(self, heat_session):
        self.heat_session = heat_session

    def stack_list(self):
        pass

    def stack_create(self):
        pass

    def stack_delete(self):
        pass

    def stack_show(self):
        pass

    def stack_update(self):
        pass

    def resource_list(self):
        pass

    def resource_create(self):
        pass

    def config_create(self):
        pass

    def config_delete(self):
        pass

    def config_show(self):
        pass
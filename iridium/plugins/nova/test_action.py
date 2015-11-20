from ...plugins.nova import NovaPluginBase


class TestAction(NovaPluginBase):
    def __new__(cls, *args, **kwargs):
        if cls is TestAction:
            raise TypeError("%s class may not be instantiated" % cls.__name__)
        return object.__new__(cls, *args, **kwargs)

    def register_path(self):
        pass

    def bar(self):
        print("this is bar.")

    def baz(self):
        print("this is baz.")
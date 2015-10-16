from iridium.libs.openstack.nova import NovaBase


class TestAction(NovaBase):
    def __new__(cls, *args, **kwargs):
        if cls is TestAction:
            raise TypeError("%s class may not be instantiated" % cls.__name__)
        return object.__new__(cls, *args, **kwargs)

    def bar(self):
        print("this is bar.")

    def baz(self):
        print("this is baz.")
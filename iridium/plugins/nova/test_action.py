from ...libs.openstack.nova import NovaExt


class TestAction(NovaExt):
    def bar(self):
        print("this is bar.")

    def baz(self):
        print("this is baz.")

from . import NovaExt


class TestAction(NovaExt):

    def register_signals(self):
        pass

    def bar(self):
        print("this is bar.")

    def baz(self):
        print("this is baz.")

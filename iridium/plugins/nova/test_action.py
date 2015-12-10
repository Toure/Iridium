from ...plugins import Plugin


class TestAction(Plugin):

    def register_signals(self):
        pass

    def bar(self):
        print("this is bar.")

    def baz(self):
        print("this is baz.")

class CustomAction(Plugin):
    def register_signals(self):
        pass
    def bza(self):
        print("welcome")
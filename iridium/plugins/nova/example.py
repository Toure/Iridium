from ...plugins import Plugin


class Example(Plugin):
    """
    Example class is how you structure a plugin for the respected components package.
    All that is needed to extend the cli base class is to inherit from the Plugin metaclass, define a registration
    method and the plugin manager will handle attaching the class as a module to the base class.
    """
    def register_signals(self):
        pass

    def foo(self):
        print('From the Example Class...')


class Foo(Plugin):
    def baz(self):
        print("Hello")
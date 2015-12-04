import os
import importlib

class PluginStore(type):
    """
    PluginStore will register plugin and place them into a list for retrieval by
    base class.
    """
    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""

        if not hasattr(cls, 'plugins'):
            # Called when the metaclass is first instantiated
            cls.plugins = []
        else:
            # Called when a plugin class is imported
            cls.register_plugin(cls)

    def register_plugin(cls, plugin):
        """Add the plugin to the plugin list and perform any registration logic"""

        # create a plugin instance and store it
        # optionally you could just store the plugin class and lazily instantiate
        instance = plugin()

        # save the plugin reference
        cls.plugins.append(instance)

        # apply plugin logic - in this case connect the plugin to blinker signals
        # this must be defined in the derived class
        instance.register_signals()

    def find_plugins(cls):
        """ Traverse registered plugin directory and import non-loaded modules  """
        # TODO complete me.
        pass

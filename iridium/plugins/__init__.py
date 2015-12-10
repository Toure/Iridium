from abc import abstractmethod
from importlib import import_module
import os


class PluginStore(type):

    """
    PluginStore will register plugin and place them into a list for retrieval by
    base class.
    """
    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""

        if not hasattr(cls, 'plugins'):
            # Called when the metaclass is first instantiated
            cls.plugins = {}
        else:
            # Called when a plugin class is imported
            cls.register_plugin(cls)

    def register_plugin(cls, plugin):
        """Add the plugin to the plugin list and perform any registration logic"""

        # create a plugin instance and store it
        # optionally you could just store the plugin class and lazily instantiate
        instance = plugin()

        # save the plugin reference
        cls.plugins[cls.__name__] = instance

        # apply plugin logic - in this case connect the plugin to blinker signals
        # this must be defined in the derived class
        instance.register_signals()


class Plugin(object, metaclass=PluginStore):

    """
    NovaExt is responsible for deriving the metaclass and to provide a
    central source for extensions.
    """
    @abstractmethod
    def register_signals(self):
        pass

    def activate_plugins(self, package_name):
        """
        Activate plugins will traverse the given package name and import the modules in the
        path.
        :param package_name: name of package to append to basedir
        :return: plugin.
        """
        import iridium.plugins
        rootdir = os.path.dirname(iridium.plugins.__file__)
        basedir = rootdir + '/' + package_name
        for basedir, dirs, files in os.walk(basedir):
            for file in files:
                if not file.startswith('__') and file.endswith('.py'):
                    file = file[0:-3]
                    print(u'iridium.plugins.{0:s}.{1:s}'.format(package_name, file))
                    return import_module(u'iridium.plugins.{0:s}.{1:s}'.format(package_name, file))

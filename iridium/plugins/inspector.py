from importlib import import_module
import os
from iridium.core.decorators import trap


class Inspector(type):

    """
    Inspector will register plugin and place them into a list for retrieval by
    base class.
    """
    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""
        cls.introspect_class(cls, attrs)

    @staticmethod
    def introspect_class(plugin: object, attrs: object) -> object:
        """Allows for injection of additional functionality
        :param attrs: attributes of class which contains a dictionary of methods and other non-callable.
        :param plugin: class object to be registered to the plugins dict.
        """
        for k in list(attrs.keys()):
            if callable(attrs[k]):
                setattr(plugin, k, trap(getattr(plugin, k)))


class Plugin(object, metaclass=Inspector):

    """
    Plugin is responsible for deriving the metaclass and to provide a
    central source for extensions.
    """

    @staticmethod
    def activate_plugins(package_name: str) -> object:
        """
        Activate plugins will traverse the given package name and import the modules in the
        path.
        :param package_name: name of package to append to basedir
        :return: plugin.
        """
        # TODO replace this logic with pkgutil.
        root_dir = os.path.abspath(os.path.dirname(__file__))
        basedir = root_dir + '/' + package_name
        for basedir, dirs, files in os.walk(basedir):
            for file in files:
                if not file.startswith('__') and file.endswith('.py'):
                    file = file[0:-3]
                    return import_module(u'iridium.plugins.{0:s}.{1:s}'.format(package_name, file))

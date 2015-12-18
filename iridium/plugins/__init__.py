from importlib import import_module
import os
from ..core.trapper import trap


class Introspect(type):

    """
    Introspect will register plugin and place them into a list for retrieval by
    base class.
    """
    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""
        cls.introspect_class(cls, attrs)

    def introspect_class(cls, klass, attrs):
        """Allows for injection of additional functionality
        :param attrs: attributes of class which contains a dictionary of methods and other non-callable.
        :param plugin: class object to be registered to the plugins dict.
        """
        for k in list(attrs.keys()):
            if callable(attrs[k]):
                setattr(klass, k, trap(getattr(klass, k)))


class Plugin(object, metaclass=Introspect):

    """
    Plugin is responsible for deriving the metaclass and to provide a
    central source for extensions.
    """

    def activate_plugins(self, package_name):
        """
        Activate plugins will traverse the given package name and import the modules in the
        path.
        :param package_name: name of package to append to basedir
        :return: plugin.
        """
        rootdir = os.path.abspath(os.path.dirname(__file__))
        basedir = rootdir + '/' + package_name
        for basedir, dirs, files in os.walk(basedir):
            for file in files:
                if not file.startswith('__') and file.endswith('.py'):
                    file = file[0:-3]
                    # print(u'iridium.plugins.{0:s}.{1:s}'.format(package_name, file))
                    return import_module(u'iridium.plugins.{0:s}.{1:s}'.format(package_name, file))

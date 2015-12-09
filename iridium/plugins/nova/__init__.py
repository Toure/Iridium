from abc import abstractmethod
from ...plugins import PluginStore
from importlib import import_module
import os


class NovaExt(object, metaclass=PluginStore):
    """
    NovaExt is responsible for deriving the metaclass and to provide a
    central source for extensions.
    """

    @abstractmethod
    def register_signals(self):
        pass

    def activate_plugins(self):
        """
        Activate plugins will traverse the given package name and import the modules in the
        path.
        :return: plugin.
        """
        root = './iridium/plugins/nova'
        for root, dirs, files in os.walk(root):
            for file in files:
                if not file.startswith('__') and file.endswith('.py'):
                    return import_module(file)

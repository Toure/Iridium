from abc import abstractmethod
from ...plugins import PluginStore
import inspect
import sys


class NovaExt(object, metaclass=PluginStore):
    """
    NovaExt is responsible for deriving the metaclass and to provide a
    central source for extensions.
    """
    def __init__(self):
       # TODO complete logic to auto import.
       #    self.clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

    @abstractmethod
    def register_signals(self):
        pass

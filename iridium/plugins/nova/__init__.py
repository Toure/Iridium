from abc import abstractstaticmethod
from ...plugins import PluginManager


class NovaPluginBase(metaclass=PluginManager):
    """
    Nova Plugin base class is the central package metaclass for all new plugins.
    """
    @abstractstaticmethod
    def register_path(self):
        """
        register path method is resposible for two things,
            1)providing a search path.
            2) registration signal for new plugin.
        :return: None
        """
        pass

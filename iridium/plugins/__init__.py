import os
import imp


class PluginManager(type):
    """ This class acts as a mount point for our plugins    """

    # Default path to search for plugins - change with register_plugin_dir
    plugin_path = os.path.join(__file__, 'plugins')

    def __init__(cls, name, bases, attrs):
        """ Initializing mount, or registering a plugin?    """
        if not hasattr(cls, 'plugins'):
            cls.plugins = PluginStruct(PluginManager)
        else:
            cls.register_plugin(cls)

    def register_plugin(self, plugin):
        """ Registration logic + append to plugins struct
        :param plugin:
        """
        plugin = plugin()  # < Init the plugin
        self.plugins[plugin.__class__.__name__] = plugin

    @staticmethod
    def register_plugin_dir(plugin_path):
        """ This function sets the plugin path to be searched
        :param plugin_path:
        """
        if os.path.isdir(plugin_path):
            PluginManager.plugin_path = plugin_path
        else:
            raise EnvironmentError('%s is not a directory' % plugin_path)

    @staticmethod
    def find_plugins():
        """ Traverse registered plugin directory and import non-loaded modules  """
        plugin_path = PluginManager.plugin_path
        if not os.path.isdir(plugin_path):
            raise EnvironmentError('%s is not a directory' % plugin_path)

        for file_ in os.listdir(plugin_path):
            if file_.endswith('.py') and file_ != '__init__.py':
                module = file_[:-3]  # < Strip extension
                mod_obj = globals().get(module)
                if mod_obj is None:
                    # TODO clean up this logic and replace imp with current importlibs
                    f, filename, desc = imp.find_module(
                        module, [plugin_path])
                    globals()[module] = imp.load_module(
                        module, f, filename, desc)


class PluginStruct(dict):
    """
        Subclass dict, re-implement __getitem__ to scan for plugins
        if a requested key is missing
    """

    def __init__(self, cls, *args, **kwargs):
        """
            Init, set mount to PlugPyMount master instance
            @param  PlugPyMount cls
        """
        self.mount = cls
        super(PluginStruct, self).__init__(*args, **kwargs)

    def __getitem__(self, key, retry=True, default=False):
        """ Re-implement __getitem__ to scan for plugins if key missing  """
        try:
            return super(PluginStruct, self).__getitem__(key)
        except KeyError:
            if default:
                return default
            elif retry:
                self.mount.find_plugins()
                return self.__getitem__(key, False)
            else:
                raise KeyError(
                    'Plugin "%s" not found in plugin_dir "%s"' % (
                        key, self.mount.plugin_path
                    )
                )

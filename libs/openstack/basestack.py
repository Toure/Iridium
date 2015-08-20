__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"


class BaseStack(object):
    """
    Base stack class is responsible for returning a list of methods from a specified module name.
    """
    def __init__(self, component):
        self.component = component

    def import_mod(self, module_name):
        """
        Import mod will return an initialized import path from the specified module name.

        :param module_name: openstack module name of interest (str).
        :return: import object of requested module name.
        """
        return __import__("libs.openstack.%s" % module_name)

    def factory(self, component):
        """
        Factory is responsible for returning a list of methods from the component name space, but
        instead of returning everything it filters out the private and built-in callables.

        :rtype : list of methods from component name space.
        """
        methodlist = [method for method in dir(component)
                      if callable(getattr(component, method)) and not method.startswith('__')]
        return methodlist

    def component_path(self):
        """
        Component path is responsible for returning the output from the closure function, which returns a method list.
        """
        return self.factory(self.import_mod(self.component))

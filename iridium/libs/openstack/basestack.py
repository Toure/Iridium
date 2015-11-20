__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from importlib import import_module


class Basestack(object):

    @staticmethod
    def import_mod(module_name):
        """
        Import mod will return an initialized import path from the specified module name.

        :param module_name: openstack module name of interest (str).
        :return: import object of requested module name.
        """
        return import_module("iridium.libs.openstack.%s" % module_name)

    def factory(self, module_object):
        """
        Factory will return a class reference object which will allow the cli to automatically instantiated
        the member when called.

        :param module_object: module which to create a reference.
        :return: factory object.
        """
        pass
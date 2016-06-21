__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from importlib import import_module
import inspect

from .keystone import create_keystone


class Basestack(object):

    @staticmethod
    def import_mod(module_name: str) -> object:
        """
        Import mod will return an initialized import path from the specified module name.

        :param module_name: openstack module name of interest (str).
        :return: import object of requested module name.
        """
        if module_name == 'keystone':
            class_name = create_keystone(version='v2')

        else:
            class_name = [obj for name, obj in inspect.getmembers(import_module(
                "iridium.libs.openstack.%s" % module_name)) if inspect.isclass(obj)][0]

        return class_name

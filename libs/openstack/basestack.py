__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"


class BaseStack(object):
    def __init__(self, component, **kwargs):
        """

        :type kwargs: authentication dictionary for keystone.
        """
        self.component = component
        self.auth_dict = kwargs


    def factory(self):
        if self.auth_dict:



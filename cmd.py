__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

import code
from libs.openstack import basestack


class Iridium(code.InteractiveConsole, basestack):
    def __init__(self):
        pass

    def shell(self, component):
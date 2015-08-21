__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from code import InteractiveConsole
from libs.openstack import basestack


class Iridium(InteractiveConsole):
    def interact(self):
        banner = "=====" * 3 + "\n" + "Welcome to Iridium" + "\n" + "VERSION: 0.1" + "\n" + "=====" * 3
        super(Iridium, self).interact(banner)

    def raw_input(self, prompt=None):
        prompt = "iridium >"
        return raw_input


class LoadFunc(Iridium, basestack):

    def findfunc(self):
        pass
        # TODO add logic to scan for modules from basestack.

    def createlocale(self):
        pass
        console = Iridium(locals=function_list)
        return console.interact()

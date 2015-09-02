__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"


from code import InteractiveConsole
from libs.openstack import basestack
from config import config
import atexit

try:
    import readline
except ImportError:
    print("readline module not found.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")


class Iridium(InteractiveConsole, object):
    """
    Iridium is the main class which subclasses from the InteractviceConsole class, this allows us to
    embed a repl into the project.
    """

    def interact(self, banner=None):
        banner = "Welcome to Iridium"
        super(Iridium, self).interact(banner)

    def raw_input(self, prompt=""):
        # TODO correct eof issue with custom prompt.
        prompt = "iridium>>> "
        return raw_input(prompt)


def save_history():
    """
    Saves the session history to specified file in config module.
    :return: None
    """
    readline.write_history_file(config.shell_history['path'])


local_modules = locals()
stack_modules = basestack.Basestack()
local_modules['nova'] = stack_modules.import_mod('nova')
local_modules['keystone'] = stack_modules.import_mod('keystone')
local_modules['ironic'] = stack_modules.import_mod('ironic')
local_modules['heat'] = stack_modules.import_mod('heat')
local_modules['swift'] = stack_modules.import_mod('swift')
local_modules['glance'] = stack_modules.import_mod('glance')
local_modules['cinder'] = stack_modules.import_mod('cinder')
local_modules['neutron'] = stack_modules.import_mod('neutron')

console = Iridium(locals=local_modules)
console.interact()

atexit.register(save_history)

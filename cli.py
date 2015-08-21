__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"


from code import InteractiveConsole
from libs.openstack import basestack

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")


class Iridium(InteractiveConsole, object):

    def interact(self, banner=None):
        banner = "Welcome to Iridium"
        super(Iridium, self).interact(banner)

    def raw_input(self, prompt=""):
        prompt = "iridium > "
        return raw_input(prompt)

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

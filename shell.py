#!/usr/bin/env python3
__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"
from IPython.terminal.interactiveshell import TerminalInteractiveShell
import atexit
import sys
from iridium.libs.openstack import basestack
from iridium.libs.trackers import tracker
from iridium.core.logger import glob_logger
from iridium.core.logger import make_timestamped_filename
from iridium.config import config

try:
    import readline
except ImportError:
    print("readline module not found.")


class Iridium(TerminalInteractiveShell):
    """
    Iridium is the main class which subclasses from the TerminalInteractiveShell class, this allows us to
    embed a repl into the project.
    """

    @staticmethod
    def enable_gui(gui=None, app=None):
        pass

    def interact(self, banner=None):
        banner = "\t\t  Welcome to\n" \
                 " ____  ____  ____  ____  ____  __  __  __  __ \n" \
                 "(_  _)(  _ \(_  _)(  _ \(_  _)(  )(  )(  \/  )\n " \
                 "_)(_  )   / _)(_  )(_) )_)(_  )(__)(  )    (\n" \
                 "(____)(_)\_)(____)(____/(____)(______)(_/\/\_)\n"

        super(Iridium, self).interact(banner)

    def raw_input(self, prompt=""):
        # TODO correct eof issue with custom prompt.
        prompt = "iridium >>> "
        return TerminalInteractiveShell.raw_input(self, prompt)


def save_history():
    """
    Saves the session history to specified file in config module.
    :return: None
    """
    # TODO figure out why this is not appending log details.
    glob_logger.info("Saving History...")
    log_path = config.logging['log_dir'] + make_timestamped_filename('iridium_cli_history')
    readline.write_history_file(log_path)


local_modules = locals()
stack_modules = basestack.Basestack
tracker_module = tracker.TrackerBase()
local_modules['nova_mod'] = stack_modules.import_mod('nova')
local_modules['keystone_mod'] = stack_modules.import_mod('keystone')
local_modules['ironic_mod'] = stack_modules.import_mod('ironic')
local_modules['heat_mod'] = stack_modules.import_mod('heat')
local_modules['swift_mod'] = stack_modules.import_mod('swift')
local_modules['glance_mod'] = stack_modules.import_mod('glance')
local_modules['cinder_mod'] = stack_modules.import_mod('cinder')
local_modules['manila_mod'] = stack_modules.import_mod('manila')
local_modules['neutron_mod'] = stack_modules.import_mod('neutron')
# TODO possibly another way to determine tracker platform.
local_modules['tracker_mod'] = tracker_module.import_mod(config.bug_tracker['tracker'])

console = Iridium(user_ns=local_modules)
console.interact()

atexit.register(save_history)

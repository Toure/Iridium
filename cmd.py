from code import InteractiveConsole
import atexit
from iridium.libs.openstack import basestack
from iridium.libs.trackers import tracker
from iridium.core.logger import glob_logger
from iridium.core.logger import make_timestamped_filename
from iridium.config.config import Config
import os

try:
    import readline
except ImportError:
    print("readline module not found.")
else:
    import rlcompleter

    readline.parse_and_bind("tab: complete")


class Iridium(InteractiveConsole, Config):
    """
    Iridium is the main class which subclasses from the TerminalInteractiveShell class, this allows us to
    embed a repl into the project.
    """

    def __init__(self, local):
        InteractiveConsole.__init__(self, locals=local)
        Config.__init__(self)
        self.log_dir_path = super().cfg_manager('log_dir')
        super().loadshell(self.load_modules())

    @staticmethod
    def enable_gui(gui=None, app=None):
        pass

    def interact(self, banner=None):
        banner = "\t\t  Welcome to\n" \
                 " ____  ____  ____  ____  ____  __  __  __  __ \n" \
                 "(_  _)(  _ \(_  _)(  _ \(_  _)(  )(  )(  \/  )\n " \
                 "_)(_  )   / _)(_  )(_) )_)(_  )(__)(  )    (\n" \
                 "(____)(_)\_)(____)(____/(____)(______)(_/\/\_)\n"
        super().interact(banner)

    def raw_input(self, prompt=""):
        prompt = "iridium >>> "
        return super().raw_input(prompt)

    def load_history(self, recall_history=False):
        """
        Load history will search the given log directory location for newest cli history file
        and inject it into the shell.
        :param recall_history: flag which instructs the manager whether or not to load previous
         history into the newly formed shell.
        :return:
        """

        if recall_history:
            os.chdir(self.log_dir_path)
            if os.getcwd() == self.log_dir_path:
                file_list = sorted(filter(os.path.isfile, os.listdir('.')),
                                   key=os.path.getmtime, reversed=True)
                glob_logger.info("Loading previous history...")
                readline.read_history_file(file_list[0])

    def save_history(self):
        # TODO figure out why this is not appending log details.
        glob_logger.info("Saving History...")
        log_path = self.log_dir_path + make_timestamped_filename('iridium_cli_history')
        readline.write_history_file(log_path)

    def load_modules(self):
        """
        Load module will construct all plugin objects for the shell enviornment, and start
        the shell.
        """
        local_modules = locals()
        stack_modules = basestack.Basestack
        tracker_module = tracker.TrackerBase()
        module_list = ['nova', 'keystone', 'ironic', 'heat', 'swift', 'glance', 'cinder', 'manila', 'neutron']

        for mod_name in module_list:
            local_modules[mod_name + '_cls'] = stack_modules.import_mod(mod_name)

        local_modules['tracker_mod'] = tracker_module.import_mod(super().cfg_manager('tracker'))
        console = Iridium(local_modules)
        console.interact()
        atexit.register(self.save_history)



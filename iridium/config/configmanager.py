__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"
import argparse
import os
import yaml
import sys

current_dir = os.path.dirname(__file__)
CONF = os.path.join(current_dir, "./iridium.yaml")


class Cli(object):

    @staticmethod
    def create_parser():
        """

        :return: Parser object
        """
        parser = argparse.ArgumentParser(description="Iridium command line interface.")
        parser.add_argument("-r", "--run-test", dest="run_test",
                            help="Run a specific test from repository.")
        parser.add_argument("-l", "--list-test", dest="list_test",
                            help="Fetch a list of current test in repository.")
        parser.add_argument("-b", "--build-test", dest="build_test",
                            help="Build test will take a list of components"
                                 "and group them into a over arching functional"
                                 "test.")
        parser.add_argument("-o", "--output", dest="output_f",
                            help="Test report output filename, format will be junit/xml.")
        parser.add_argument("-c", "--credential", dest="creds",
                            help="File which contains credentials for keystone.")
        parser.add_argument("-s", "--shell", action="store_true", default=False, dest="shell",
                            help="Start interactive shell session.")
        parser.add_argument("-au", "--auth_url", dest="auth_url",
                            help="URL of the controller which to attach.")
        parser.add_argument("-ld", "--log_dir", dest="log_dir",
                            help="Path for Iridium to store log files.")
        parser.add_argument("-fl", "--function_call_log", dest="fn_call_log",
                            help="Name of the replay function call "
                                 "log")
        parser.add_argument("-bt", "--bug_tracker", dest="b_tracker",
                            help="Name of given bug track system."
                                 "Supported ones are Bugzilla and Launchpad.")

        if len(sys.argv) == 1:
            parser.print_help()
            exit(1)
        else:
            return parser.parse_args()


class ConfigManager(Cli):
    def __init__(self):
        Cli.__init__(self)
        self.args = self.create_parser()

    def load_shell(self, shell_function):
        """
        This method will start the interactive is the Bool is
        passed on the command line.
        :param shell_function: function responsible for spawning the interactive shell
        (load_modules).
        """
        if self.args.shell:
            shell_function()

    def cfg_manager(self, key, collection=CONF):
        """
        ConfigManager manager will search configurations file and cli for a given key and give precedence to the non-Null
        value from the cli.
        :param collection: yaml file which contains configuration data.
        :param key: search value to lookup in yaml structure.
        :return: value of corresponding key.
        """
        coll = self.dump_config(collection)
        config_value = self.lookup(coll, key)
        cli_value = self.lookup(vars(self.args), key)

        if cli_value is not None:
            return cli_value
        else:
            return config_value

    def lookup(self, config_dict: dict, search_key: str) -> object:
        """
        lookup will search the given collection for a specified key and return
        its value.
        :param search_key: key in specified collection.
        :param config_dict: dictionary which contains the search key.
        :return: value of search_key.
        """
        if search_key in config_dict:
            return config_dict[search_key]
        for k, v in config_dict.items():
            if isinstance(v, dict):
                item = self.lookup(v, search_key)
                if item is not None:
                    return item

    @staticmethod
    def dump_config(config_obj):
        with open(config_obj, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as ye:
                print(ye)

    def update_config(self, config_obj):
        # TODO add function to perform persistent update of yaml file.
        pass

    @staticmethod
    def write_config(config_dict: dict, fname: str) -> None:
        """
        Write config will dump the above yaml defaults into the users .config/Iridium directory.
        :param config_dict: name of the map which will be dumped as a yaml file.
        :param fname: name of output yaml file.
        :return: config.yaml
        """
        with open(fname, "w") as cfg_stream:
            yaml.dump(config_dict, cfg_stream)
            cfg_stream.write("\n")
        cfg_stream.close()


class Dispatch(Cli):
    def __init__(self):
        super().__init__()

    def list_test(self):
        """
        List test will display current configured tetst.
        :return:
        """
        pass

    def run_test(self, testname):
        """
        Run test will dispatch given test name.
        :return:
        """
        pass

    def build_test(self, testlist):
        """
        Build test will take a list of test names and create a group
        functional test.
        :param testlist:
        :return:
        """
        pass

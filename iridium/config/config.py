__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"
import argparse
import confuse
import sys
import yaml

CONF = """
--- Openstack base configurations for API services.
auth_info:
  v2:
    auth_url: 'http://localhost:5000/v2.0/'
    username: 'admin'
    password: '60b170ff33d84278'
    tenant_name: 'admin'
  v3:
    auth_url: 'http://localhost:5000/v3'
    username: 'admin'
    password: 'password'
    project_name: 'admin'
    user_domain_name: 'default'
    project_domain_name: 'default'

logging:
  log_dir: '/tmp/iridium_logs/'

rdo_clones:
  base: '/tmp/rdo_clones/'

bug_tracker:
  tracker: 'bugz'

iridium_function_call:
  function_log: '/tmp/iridium_logs/iridium_func_call.yml'
"""


class Cli(object):
    def __init__(self, shell_fn):
        self.shell_fn = shell_fn
        self.cfg = confuse.LazyConfig('Iridium')

    def write_config(self):
        """
        Write config will dump the above yaml defaults into the users .config/Iridium directory.
        :return: config.yaml
        """
        import yaml
        with open("~/.config/Iridium/config.yaml", "w") as cfg_stream:
            yaml.dump(CONF, cfg_stream)
            cfg_stream.write("\n")
        cfg_stream.close()

    def config(self):
        """

        :return:
        """
        cli_args = self.cli()
        if cli_args.shell:
            # call the function responsible for starting the interactive shell.
            self.shell_fn()
        else:
            self.cfg.set_args(cli_args)

    def cli(self):
        """
        Command line interface will be responsible for providing the end user a way to interact with builtin test or
        start a interactive shell.
        :return:
        """
        parser = argparse.ArgumentParser(description="Iridium command line interface.")
        parser.add_argument("-r", "--run-test", dest="run_test", help="Run a specific test from repository.")
        parser.add_argument("-l", "--list-test", dest="list_test", help="Fetch a list of current test in repository.")
        parser.add_argument("-b", "--build-test", dest="build_test", help="Build test will take a list of information"
                                                                          "to")
        parser.add_argument("-o", "--output", dest="output_f",
                            help="Test report output filename, format will be junit/xml.")
        parser.add_argument("-c", "--credential", dest="creds", help="File which contains credentials for keystone.")
        parser.add_argument("-s", "--shell", action="store_true", default=False, dest="shell",
                            help="Start interactive shell session.")
        parser.add_argument("-au", "--auth_url", dest="auth_url", help="URL of the controller which to attach.")
        parser.add_argument("-ld", "--log_dir", dest="log_dir", help="Path for Iridium to store log files.")
        parser.add_argument("-fl", "--function_call_log", dest="fn_call_log", help="Name of the replay function call "
                                                                                   "log")
        parser.add_argument("-bt", "--bug_tracker", dest="b_tracker", help="Name of given bug track system."
                                                                           "Supported ones are Bugzilla and Launchpad.")
        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)

        return parser.parse_args()



class Config(object):

    def cfg_manager(self, key, collection=CONF):
        """
        Config manager will search configurations file or input depending on keyword passed.
        :param collection: yaml file which contains configuration data.
        :param key: search value to lookup in yaml structure.
        :return: value of corresponding key.
        """
        coll = self.dump_config(collection)
        return self.lookup(coll, key)

    def lookup(self, coll: dict, search_key: str) -> object:
        """
        lookup will search the given collection for a specified key and return
        its value.
        :param search_key: key in specified collection.
        :param coll: dictionary which contains the search key.
        :return: value of search_key.
        """
        if search_key in coll:
            return coll[search_key]
        for k, v in coll.items():
            if isinstance(v, dict):
                item = self.lookup(v, search_key)
                if item is not None:
                    return item

    def dump_config(self, config_obj):
        with open(config_obj, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as ye:
                print(ye)

    def update_config(self, config_obj):
            # TODO add function to perform persistent update of yaml file.
        pass

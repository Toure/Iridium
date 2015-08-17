__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from cmd2 import Cmd
from libs.openstack import keystone

class Rhea(Cmd):
    """Command processor which will allow users to test Features of Openstack Deployment
    from a command line shell, it will also have the ability to save config as an output for
    test plans."""
    prompt = 'Rhea > '
    intro = "Command line environment which enables functional testing."

    def do_setup(self, line):
        """
        Setup will be responsible for configuring services and openstack
        instances.
        :param line:
        :return:
        """
        print "hello"

    def do_deploy(self, line):
        """
        Deploy will install an openstack instances based on saved config.
        :param line:
        :return:
        """
        return True

    def do_config(self, arg):
        """
        Configu will switch name space to allow for the creation of a .
        :param arg:
        :return:
        """
        pass

    def do_auth(self, args):
        """
        Auth will be responsible for creating the keystone object from the command line.
        :param args:
        :return: keystone session for the command line.
        """
        keystone.create_keystone(args)


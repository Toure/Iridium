import os
import importlib
import sys

from iridium import core
from iridium.config import config


def add_client_to_path(base_dir=None, debug=False, base_clients=None):
    """
    Can set the python sdk clients.  If git is set to True, then base_dir must
    have a valid directory pointing to the folder where the projects were cloned
    to.  By default, base_clients will import the keystone, nova and glance
    python-{}client modules.

    :param base_dir: Only needed if git=True. The folder where the git cloned
                     clients are
    :param git: If set to False, use the regular yum or pip installed module,
                if True, use git cloned modules
    :param base_clients: A sequence of python-{}clients to import

    :return: the final sys.path
    """
    client = "{}client"
    if base_clients is None:
        base_clients = ["glance", "keystone", "nova"]

    if base_dir and not os.path.isdir(base_dir):
        raise core.exceptions.ArgumentError("{} does not exists".format(base_dir))

    if debug:
        client = "python-{}client"
        if base_dir is None:
            # use the location from smog_config.yml
            base_dir = config.rdo_clones['base']

        if not os.path.isdir(base_dir):
            raise Exception("Unable to find base directory to load modules {}".format(base_dir))

        extra = [os.path.join(base_dir, client.format(x)) for x in base_clients]
        for d in extra:
            if not os.path.isdir(d):
                raise core.exceptions.ArgumentError("{} does not exist".format(d))
        sys.path = extra + sys.path
    else:
        clients = map(client.format, base_clients)
        map(importlib.import_module, clients)

    return sys.path

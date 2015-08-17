__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from ironicclient import client
import keystone


def create_ironic_obj(version, **kwargs):
    ironic_obj = client.get_client(keystone.create_keystone(version, **kwargs))

    return ironic_obj


def baremetal_list(version, **kwargs):
    ironic = create_ironic_obj(version, **kwargs)

    return ironic.list_nodes()

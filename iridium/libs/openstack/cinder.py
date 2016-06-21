__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from cinderclient import client
from iridium.libs.openstack import keystone
from iridium.plugins.inspector import Plugin


class CinderBase(object):
    """
    CinderBase class is used for standard commands which can be issued to cinder.
    example: create or delete a volume -- cinder create --name=test_volume 10
    """

    def __init__(self, version: int, kwargs: dict) -> object:
        """
        :param kwargs valid keys are username, password, tenant_name, auth_url.
        :return: cinder auth object.
        """
        ks_kwargs = keystone.keystone_retrieve(**kwargs)
        cinder_auth = [ks_kwargs[key] for key in ["username", "password", "tenant_name", "auth_url"]]
        self.cinder_session = client.Client(version, *cinder_auth)
        plugin = Plugin()
        self.extension = plugin.activate_plugins('cinder')

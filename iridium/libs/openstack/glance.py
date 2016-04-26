__author__ = "Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "stoner@redhat.com"
__status__ = "Alpha"

from iridium.core.exceptions import ArgumentError
from iridium import add_client_to_path
from iridium.plugins import Plugin

DEBUG = False
add_client_to_path(debug=DEBUG)

from glanceclient import Client as GlanceFactory
from iridium.libs.openstack import keystone


class GlanceError(Exception):
    pass


class GlanceBase(object):
    def __init__(self, version: int) -> object:
        self.keystone_cl = keystone.create_keystone()
        if version not in ["1", "2"]:
            raise ArgumentError("Invalid glance version choice")

        url_for = self.keystone_cl.service_catalog.url_for
        glance_endpt = url_for(service_type="image", endpoint_type="publicURL") + "/v" + version
        self.glance_session = GlanceFactory(endpoint=glance_endpt,
                                            token=self.keystone_cl.auth_token)
        plugin = Plugin()
        self.extension = plugin.activate_plugins('glance')

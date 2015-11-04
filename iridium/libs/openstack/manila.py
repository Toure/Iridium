__author__  = 'Dustin Schoenbrun'
__license__ = 'Apache License 2.0'
__version__ = '0.1'
__email__   = 'dschoenb@redhat.com'
__status__  = 'Alpha'

from keystoneclient.auth.identity import v2
from keystoneclient import session
from manilaclient import client
from iridium.libs.openstack import keystone

class ManilaBase(object):
    """
    ManilaBase is used for commands that can be issued to Manila.
    """

    def __init__(self, client_version, **kwargs):
       """
       Get the Keystone credentials and use them to create the Manila client.
       :param client_version: The version of the Manila Client to use as a string (e.g. '2.0')
       :param kwargs: Keystone authentication parameters. We need to have:
            auth_url: The URL for Keystone Authentication
            username: The username to use for Keystone authentication
            password: The password for the user specified in username.
            tenant_name: The name of the tenant that will be used for Keystone authentication
       """
       keystone_args = keystone.keystone_retrieve(**kwargs)
       keystone_authorization = v2.Password(**keystone_args)
       keystone_session = session.Session(auth=keystone_authorization)
       self.manila_session = client.Client(client_version, session=keystone_session)


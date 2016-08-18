__author__ = 'Dustin Schoenbrun'
__license__ = 'Apache License 2.0'
__version__ = '0.1'
__email__ = 'dschoenb@redhat.com'
__status__ = 'Alpha'

from manilaclient import client
from iridium.libs.openstack import keystone
from iridium.plugins.inspector import Plugin


class ManilaBase(object):
    """
    ManilaBase is used for basic commands that can be issued to Manila. This will involve basic operations on shares,
    share networks, share snapshots, share types, and other Manila constructs.
    """

    def __init__(self, client_version: str = '2.0', keystone_version: str = 'v2'):
        """
       Get the Keystone credentials and use them to create the Manila client.
       :param client_version: The version of the Manila Client to use as a string (e.g. '2.0')
       :param keystone_version: The version of the Keystone API to use for authentication.
       """
        keystone_credentials = keystone.keystone_retrieve(version=keystone_version)
        self.manila_session = client.Client(client_version, *keystone_credentials)

    def __getattr__(self, item):
        """
        getattr is responsible for searching requested methods which exist in the
        plugin tree.
        :param item: name of method
        :return: remote method.
        """
        __plugin = Plugin()
        __ext = __plugin.activate_plugins('manila')
        return getattr(__ext.Common(self.manila_session), item)

    def create_share(self, protocol: str, size: int = 1, share_type: str = None) -> object:
        """
        Create a Manila share with the specified protocol, size (in GB), and share type
        :param protocol: The protocol to be used for accessing the share. Valid values are nfs, cifs, glusterfs,
        hdfs, and cephfs
        :param size: The integer size of the share in gigabytes
        :param share_type: The Manila share type of the share.
        :return: The share object that was created
        """
        self.manila_session.share.create(protocol, size, share_type=share_type)

    def update_share(self, share_id: str, **kwargs):
        """
        Update an existing Manila share with the specified share ID.
        :param share_id: The UUID of the share to be updated.
        :param kwargs: The new values for modifiable aspects of the share.
        :return: The share object that was modified.
        """
        self.manila_session.share.update(share_id, kwargs)

    def get_share_info(self, share_id: str):
        """
        Get a detailed dictionary of information about the specified share.
        :param share_id: The UUID of the share to get the information from
        :return: A dictionary containing the detailed attributes of the specified share.
        """
        self.manila_session.share.get(share_id)

    def list_shares(self):
        """
        List the shares visible to the current Keystone Project.
        :return: A list of shares that are visible to the current Keystone Project.
        """
        self.manila_session.share.list()

    def delete_share(self, share_id: str):
        """
        Delete the specified share.
        :param share_id: The UUID of the share to be deleted.
        :return:
        """
        self.manila_session.shares.delete()
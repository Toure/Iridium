from iridium.plugins.inspector import Plugin


class Common(Plugin):
    def __init__(self, manila_session):
        self.manila_session = manila_session

    def create_share(self, size, protocol, **kwargs):
        """
        Create a share of the specified size (in GB) and protocol.
        TODO: Figure out if kwargs is fine or if I should enumerate all the parameters
        :param size: The size of the share in GB
        :param protocol: The protocol that the share will use
        :param kwargs: Dictionary specifying other, optional parameters for a share.
        :return:
        """
        pass

    def update_share(self, share_id, **kwargs):
        """
        Update a share with the given ID. kwargs can contain any number of modifiable elements of a share
        :param share_id: The ID of the share to be modified
        :param kwargs:  The dictionary specifying the elements that need to be modified.
        :return:
        """
        pass

    def show_share(self, share_id, **kwargs):
        """
        Show the details of a share with the given ID.
        :param share_id: The share to get the information from.
        :param kwargs: Any optional parameters for the filtering of information from the share.
        :return:
        """
        pass

    def list_shares(self, **kwargs):
        """
        List all shares present for the current environment
        :param kwargs: Any optional filtering options for the shares.
        :return:
        """

    def delete_share(self, share_id):
        """
        Delete the share with the given ID.
        :param share_id: The ID of the share to be deleted.
        :return:
        """
        pass

    def create_snapshot(self, share_id, **kwargs):
        """
        Create a snapshot of the specified share.
        :param share_id: The ID of the share to be snapshotted
        :param kwargs: Any additional parameters for the creation of a snapshot.
        :return:
        """
        pass

    def update_snapshot(self, snapshot_id, **kwargs):
        """
        Update a snapshot with the specified ID with the information contained within kwargs
        :param snapshot_id: The ID of the snapshot to update
        :param kwargs: A dictionary of parameters to update in the snapshot.
        :return:
        """

    def create_share_type(self, name, driver_handles_share_servers, **kwargs):
        """
        Create a share type with the specified name and the specified support for handling share servers or not.
        :param name: The name of the share type.
        :param driver_handles_share_servers: Boolean value for whether or not the driver handles the creation of
        share severs.
        :param kwargs: A dictionary of additional parameters for share type creation.
        :return:
        """
        pass

    def update_share_type(self, share_type_id, **kwargs):
        """
        Update a share type with the specified ID with the information contained within kwargs
        :param share_type_id: The ID of the share type to update
        :param kwargs: A dictionary specifying the elements that need to be modified
        :return:
        """
        pass

    def show_share_type(self, share_type_id, **kwargs):
        """
        Show the details of a share type with the given ID
        :param share_type_id: The ID of the share type to be shown.
        :param kwargs: Any optional parameters for the filtering of information from the share.
        :return:
        """
        pass

    def list_share_types(self, **kwargs):
        """
        List all share types present in the current environment
        :param kwargs: Any optional filtering options for the share types
        :return:
        """
        pass

    def delete_share_type(self, share_type_id):
        """
        Delete the share type with the given ID
        :param share_type_id: The ID of the share type to be deleted.
        :return:
        """
        pass
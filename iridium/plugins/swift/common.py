from iridium.plugins import Plugin
from pprint import pprint


class Common(Plugin):
    """
    """
    def __init__(self, swift_session):
        self.swift_session = swift_session

    def list_container(self):
        """
        List all available containers.

        :return: list of container names.
        """
        container_info = self.swift_session.get_account(self.storage_location, self.ks.auth_token)
        container_list = [container_info[1][count]['name'] for count in range(len(container_info[1]))]
        return container_list

    def create_container(self, container_name):
        """
        Creates a container based on name given.

        :param container_name: name of container to create.
        :return: progress information of container creation.
        """
        self.swift_session.put_container(self.storage_location, self.ks.auth_token, container_name)
        status = self.container_status(self.storage_location, self.ks.auth_token, container_name)
        pprint(status)

    def container_status(self, url, token, container_name):
        """
        Returns status of container.

        :param url: storage url.
        :param token: auth token from keystone.
        :param container_name: name of container to return status.
        :return: dict of information on specified container.
        """
        status = self.swift_session.head_container(url, token, container_name)
        return status

    def delete_container(self, container_name):
        """

        :param container_name:
        :return:
        """
        ret = self.swift_session.delete_container(self.storage_location, self.ks.auth_token, container_name)
        if ret is None:
            print('Container: %s has been deleted.' % container_name)


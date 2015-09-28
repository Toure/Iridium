from swiftclient import client as sc
from iridium.libs.openstack import keystone
from pprint import pprint


class SwiftBase(object):
    def __init__(self):
        self.ks = keystone.create_keystone()
        self.storage_location = sc.Connection(authurl=self.ks.auth_url,
                                              user=self.ks.username,
                                              key=self.ks.password,
                                              tenant_name=self.ks.tenant_name,
                                              auth_version='2.0').get_auth()[0]

    def list_container(self):
        """
        List all available containers.

        :return: list of container names.
        """
        container_info = sc.get_account(self.storage_location, self.ks.auth_token)
        container_list = [container_info[1][count]['name'] for count in range(len(container_info[1]))]
        return container_list

    def create_container(self, container_name):
        """
        Creates a container based on name given.

        :param container_name: name of container to create.
        :return: progress information of container creation.
        """
        sc.put_container(self.storage_location,
                         self.ks.auth_token,
                         container_name)
        status = self.container_status(self.storage_location,
                                       self.ks.auth_token, container_name)
        pprint(status)

    @staticmethod
    def container_status(url, token, container_name):
        """
        Returns status of container.

        :param url: storage url.
        :param token: auth token from keystone.
        :param container_name: name of container to return status.
        :return: dict of information on specified container.
        """
        status = sc.head_container(url, token, container_name)
        return status

    def delete_container(self, container_name):
        """

        :param container_name:
        :return:
        """
        ret = sc.delete_container(self.storage_location, self.ks.auth_token, container_name)
        if ret is None:
            print('Container: %s has been deleted.' % container_name)

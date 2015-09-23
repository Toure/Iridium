__author__ = "Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "stoner@redhat.com"
__status__ = "Alpha"

import os

from iridium.core.exceptions import ArgumentError
from iridium import add_client_to_path
from iridium.core.downloader import Downloader

DEBUG = False
add_client_to_path(debug=DEBUG)

from glanceclient import Client as GlanceFactory
from iridium.libs.openstack import keystone


class GlanceError(Exception):
    pass


class GlanceBase(object):
    def __init__(self, version):
        self.keystone_cl = keystone.create_keystone()
        if version not in ["1", "2"]:
            raise ArgumentError("Invalid glance version choice")

        url_for = self.keystone_cl.service_catalog.url_for
        glance_endpt = url_for(service_type="image", endpoint_type="publicURL") + "/v" + version
        self.glance_session = GlanceFactory(endpoint=glance_endpt,
                                            token=self.keystone_cl.auth_token) 

    def glance_image_list(self):
        """

        :param self: glance client
        :return: returns a generator object to list through
        """
        return self.glance_session.images.list()

    @staticmethod
    def glance_images_by_name(name, images):
        """
        Helper function to find an image by name given the image generator

        :param name:
        :param images:
        :return:
        """
        accum = []
        for x in list(images):
            if x.name == name:
                accum.append(x)
        return accum

    @staticmethod
    def glance_filter_image(images, sort_fn=None):
        if sort_fn is None:
            sort_fn = lambda i: True
        return [x for x in images if sort_fn(x)]

    def glance_delete_image(self, filt_fn):
        """
        Deletes an image for a given filter function

        :param filt_fn:
        :return:
        """
        imgs = filt_fn(self.glance_session.glance_image_list())
        for i in imgs:
            i.delete()

    def create_image(self, path, img_name, public=True, disk_format="qcow2",
                     container_format="bare", properties=None):
        """
        Creates a new glance image

        :param glance_cl: a glance object (return from create_glance)
        :param path: path to the image file
        :param img_name: name to give the image
        :param public: boolen to determine set the is_public for image
        :param disk_format: str that determines the image (ie "raw" or "qcow2")
        :param container_format: str to describe the container (eg "bare")
        :return:
        """
        # create the rescue image with the actual data from the binary file
        if not os.path.isfile(path):
            raise ArgumentError("{} is not a valid image".format(path))

        with open(path, "rb+") as fimage:
            self.glance_session.images.create(name=img_name, is_public=public, data=fimage,
                                             disk_format=disk_format, properties=properties,
                                             container_format=container_format)

        # stupidly, the python-glanceclient Image.create() does not return anything
        # so let'nova_tests figure out if it was successful or not and return the newly
        # created glance image
        images = self.glance_image_list()
        img = self.glance_images_by_name(img_name, images)
        if not img:
            raise GlanceError("Could not find image that was created")
        return img[0]

    def update_image(self, properties):
        """
        Updates the image with the new properties

        :param properties:
        :return:
        """
        return self.glance_session.update(**properties)

    def set_image_property(self, img, meta):
        """
        Updates the image properties

        This can be used when for example you need to create a "fake"
        windows VM.

        Usage::

            base = BaseStack()
            img = glance.create_image(base.glance, "/tmp/cirros.qcow2", "fake-ms",
                                      disk_format="qcow2", properties=None)
            properties = {"os_distro": "windows"}
            ms_img = glance.set_image_property(properties)
            guest = base.boot_instance(img=ms_img, name="fake-windows")

        :param img:
        :param meta:
        :return:
        """
        return img.update_image(img, properties=meta)

    def get_cloud_image(self, location, name):
        # Download a cirros image
        if not os.path.exists(location):
            if not Downloader.download_url(location, "/tmp", binary=True):
                raise Exception("Could not download cirros image")
            else:
                location = "/tmp/" + name
        return location

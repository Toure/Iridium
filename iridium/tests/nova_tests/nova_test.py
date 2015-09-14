__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

import pytest
from libs.openstack import nova
from iridium.core.logger import glob_logger
from iridium.core.exceptions import AmbiguityException

@pytest.mark.create_instance
def test_instance_creation():
    nova_cl = nova.NovaBase('2')
    glob_logger.info("Nova instance creation test...")
    for nodes in range(10):
        glob_logger.info("Creating node: %s" % nodes)
        try:
            nova_cl.boot_instance()
        except AmbiguityException:
            print("Not sure the status of new instances.")


def test_instance_shutdown():
    pass


def test_instance_deletion():
    pass


def test_instance_migration():
    pass


def test_instance_volume_attach():
    pass


def test_instance_configuration():
    pass

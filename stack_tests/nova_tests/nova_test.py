__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

import pytest
from iridium.libs.openstack import nova
from iridium.core.logger import glob_logger


@pytest.mark.create_instance
def test_instance_creation():
    nova_cl = nova.NovaBase('2')
    glob_logger.info("Nova instance creation test...")
    assert nova_cl.list_instances()


@pytest.mark.instance_shutdown
def test_instance_shutdown():
    pass


@pytest.mark.instance_delete
def test_instance_deletion():
    pass


@pytest.mark.instance_migrate
def test_instance_migration():
    pass


@pytest.mark.instance_volume_attach
def test_instance_volume_attach():
    pass

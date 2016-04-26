__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

import pytest
from iridium.libs.openstack import nova
from iridium.core.logger import glob_logger


@pytest.fixture
def nova_auth():
    nova_cl = nova.NovaBase('2')
    return nova_cl

@pytest.mark.create_instance
def test_instance_creation(nova_auth):
    glob_logger.info("Nova instance creation test...")
    #assert nova_auth.boot_instance('iridium_test', '6348bd72-602f-41ce-99fa-49c6789bbeb3', '1')
    assert nova_auth.boot_instance('iridium_test', '22b40f63-2b37-4855-8f32-07da65bd3c43', '1')

@pytest.mark.create_multiple_instances
def test_instance_create_multi(nova_auth):
    glob_logger.info("Nova multi instance create.")
    for node in range(10):
        nova_auth.boot_instance('iridium_test_%s' % node, '6348bd72-602f-41ce-99fa-49c6789bbeb3', '1')
    else:
        assert 0
    glob_logger.info("Complete Nove multi create.")

@pytest.mark.list_instances
def test_instance_list(nova_auth):
    glob_logger.info("Nova instance list test.")
    print(nova_auth.list_instances())
    glob_logger.debug('List of instances: %s' % list)


@pytest.mark.instance_shutdown
def test_instance_shutdown():
    pass


@pytest.mark.instance_delete
def test_instance_deletion(nova_auth):
    pass



@pytest.mark.instance_migrate
def test_instance_migration():
    pass


@pytest.mark.instance_volume_attach
def test_instance_volume_attach():
    pass

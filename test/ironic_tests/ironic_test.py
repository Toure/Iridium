__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

import pytest


# Chassis test.
@pytest.mark.chassis
def test_create_chassis():
    pass


@pytest.mark.chassis
def test_list_chassis():
    pass


@pytest.mark.chassis
def test_delete_chassis():
    pass


# Driver test.
@pytest.mark.driver
def test_driver_list():
    pass


@pytest.mark.driver
def test_driver_update():
    pass


@pytest.mark.driver
def test_driver_delete():
    pass


@pytest.mark.driver
def test_driver_properties():
    pass


@pytest.mark.driver
def test_driver_get():
    pass


@pytest.mark.driver
def test_driver_update():
    pass


# Node test.
@pytest.mark.node
def test_node_list():
    pass


@pytest.mark.node
def test_node_port_list():
    pass


@pytest.mark.node
def test_node_get():
    pass


@pytest.mark.node
def test_node_get_by_uuid():
    pass


@pytest.mark.node
def test_node_create():
    pass


@pytest.mark.node
def test_node_delete():
    pass


@pytest.mark.node
def test_node_update():
    pass


@pytest.mark.node
def test_node_set_state():
    pass


# Port test.
@pytest.mark.port
def test_port_list():
    pass


@pytest.mark.port
def test_port_create():
    pass


@pytest.mark.port
def test_port_get():
    pass


@pytest.mark.port
def test_port_get_by_address():
    pass


@pytest.mark.port
def test_port_delete():
    pass


@pytest.mark.port
def test_port_update():
    pass

__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from ironicclient import client
from ironicclient.v1 import chassis
from ironicclient.v1 import node
from ironicclient.v1 import port
from libs.openstack import keystone


class IronicBase(object):
    def __init__(self):
        self.chassis = chassis.ChassisManager
        self.node = node.NodeManager
        self.port = port.PortManager

    def chassis_create(self, **kwargs):
        self.chassis.create(**kwargs)

    def chassis_delete(self, chassis_id):
        self.chassis.delete(chassis_id)

    def chassis_list(self):
        self.chassis.list()

    def node_create(self, **kwargs):
        self.node.create(**kwargs)

    def node_delete(self, node_id):
        self.node.delete(node_id=node_id)

    def node_list(self):
        self.node.list()

    def node_update(self, node_id, patch):
        self.node.update(node_id=node_id, patch=patch)

    def port_create(self, **kwargs):
        self.port.create(**kwargs)

    def port_delete(self, port_id):
        self.port.delete(port_id=port_id)

    def port_list(self):
        self.port.list()

    def port_show(self):
        self.port.list(detail=True)

__author__ = 'toure'


from swiftclient import client
from iridium.libs.openstack import keystone

class SwiftBase(object):
    def __init__(self):
        creds = keystone.keystone_retrieve()

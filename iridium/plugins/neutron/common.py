from iridium.plugins.inspector import Plugin
from iridium.core.exceptions import AmbiguityException


class Common(Plugin):
    def __init__(self, neutron_session):
        self.neutron_session = neutron_session

    def list_neutron_nets(self, neutron_session, filter_fn=None):
        """
        Lists the neutron_tests networks on this deployment

        :param neutron_session: neutron_tests Client object
        :param filter_fn: a predicate fn (see has_network_field)
        :return: a list of networks filtered through the filter_fn
        """
        nets = self.neutron_session.list_networks()["networks"]
        if filter_fn:
            nets = list(filter(filter_fn, nets))
        return nets

    def has_network_field(self, value, key="name"):
        """
        Returns a function usable as a filter to list_neutron_nets

        Usage::

          active_pred = has_network_field("ACTIVE", key="status")
          nets = list_neutron_nets(neutron_session, filter_fn=active_pred)

        :param value: The value (of key) to match against
        :param key: the key in the network object to look up
        :return: a predicate function that takes a network object (a dict of
                 this form:

                 {'admin_state_up': True,
                   'id': 'bbcafa75-296a-4a20-bb57-4a0f12ef4bc4',
                   'mtu': 0,
                   'name': 'public',
                   'provider:network_type': 'vxlan',
                   'provider:physical_network': None,
                   'provider:segmentation_id': 10,
                   'router:external': True,
                   'shared': True,
                   'status': 'ACTIVE',
                   'subnets': ['55d174f0-bed4-4699-a4ff-1b738ac50207'],
                   'tenant_id': '85da67eac420401a960ff47c9c2f3469'}

                and returns net_obj[key] == value

        """

        def find(net):
            return net[key] == value

        return find

    def get_network_uuid(self, neutron_session, name="private", no_ambiguity=True):
        """
        Retrieves the network UUID from neutron_tests with the matching name.

        If no_ambiguity is True, and there are more than one networks with the same
        name, raise an AmbiguityException.  If no_ambiguity is False, return the
        first network with this name found.

        :param neutron_session: a neutron_tests client
        :param name: (str) name of the network (eg "public")
        :return: the UUID (str) of the network from neutron_tests
        """
        name_pred = self.has_network_field(name)
        nets = self.list_neutron_nets(neutron_session, filter_fn=name_pred)

        if len(nets) > 1 and no_ambiguity:
            err = "Found more than one net: ".format(nets)
            raise AmbiguityException(err)

    class NIC:
        """
        Defines a network object that can be used for a nova boot:

        - net-id: net-uuid
        - v4-fixed-ip: IPv4-addr
        - v6-fixed-ip: IPv6-addr
        - port-id: port-uuid

        """

        def __init__(self, net_id=None, v4=None, v6=None, port_id=None):
            self.net_id = net_id
            self.v4 = v4
            self.v6 = v6
            self.port_id = port_id

        def to_dict(self):
            """
            Uggghh, so python can't use dashes in symbols, but the keywords in
            the dict have dashes.

            :return: dict
            """
            valid = {"net-id": self.net_id,
                     "v4-fixed-ip": self.v4,
                     "v6-fixed-ip": self.v6,
                     "port-id": self.port_id}
            return valid
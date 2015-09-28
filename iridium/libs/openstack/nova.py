__author__ = 'toure'

import itertools
import os
import json
import time

import httplib2
import novaclient.client as nvclient
from novaclient.exceptions import NotFound

from iridium.libs.openstack import keystone
from iridium.core.logger import glob_logger


class NovaBase(object):
    def __init__(self, version='2', **kwargs):
        creds = keystone.keystone_retrieve(version='v2')
        nova_cred_list = [creds[key] for key in ["username", "password", "tenant_name", "auth_url"]]
        self.nova_session = nvclient.Client(version, *nova_cred_list)

    def delete_server(self, compute_instance):
        """

        :param compute_instance:
        :return:
        """
        server = self.nova_session.servers.find(name=compute_instance)
        server.delete()

    def boot_instance(self, server_name, server_image, flavor, count=1, **kwargs):
        """
        Boots up a compute instance

        So, in kilo you now have to specify a neutron_tests network ID

        :param server_name: string of name to give to compute instance
        :param server_image: the nova image object to boot up
        :param flavor: the flavor
        :return: instance if successful, None otherwise
        """
        if count == 1:
            default = dict([("name", server_name), ("image", server_image),
                            ("flavor", flavor)])
            if not kwargs:
                kwargs = default
            else:
                kwargs.update(default)

            instance = self.nova_session.servers.create(**kwargs)
            servers = self.nova_session.servers.list()
            for s in servers:
                if s.name == server_name:
                    return instance
            else:
                glob_logger.error("Base image did not boot up")
                return None
        else:
             for node in count:
                 node_name = server_name + str(node)
            self.boot_instance(node_name, server_image, flavor)

    def add_keypair(self, name, pubkey):
        """
        Creates a keypair for nova to use

        :param name: (str) name to give the keypair
        :param pubkey: (str) path to the public key to use
        :return:
        """
        if os.path.exists(pubkey):
            with open(pubkey, "r") as pub:
                txt = pub.read()
        else:
            txt = pubkey
        kp = self.nova_session.keypairs.create(name, public_key=txt)
        return kp

    def add_sg_rule(self, parent, proto="tcp", from_port=22, to_port=22, cidr=None,
                    group_id=None):
        """
        Creates a new security group rule which is necessary if you want to ping or
        ssh into an instance.

        Usage::

            # Create ssh rule
            base = BaseStack()
            sg = base.nova.security_groups.find(name="default")
            rule = add_sg_rule(base.nova, sg.id, proto="tcp", from_port=22,
                              to_port=22)

        :param parent: the security group id to associate the rule with
        :param proto: (str) one of tcp, udp, icmp etc
        :param from_port: (int) start port range
        :param to_port: (int) end port range
        :param cidr: the cidr classification
        :param group_id: source security group to apply to rule
        :return:
        """
        sg = self.nova_session.security_group_rules
        res = sg.create(parent, ip_protocol=proto, cidr=cidr, from_port=from_port,
                        to_port=to_port, group_id=group_id)
        return res

    # AFAICT, the rescue operation with the added feature doesn't
    # seem to be in the python-novaclient, so let'nova_tests make our own function for now
    def rescue_alt_image(self, server_id, admin_pw=None, rescue_id=None, version='v2'):
        """
        Performs a rescue by replacing the compute instance with an alternate rescue
        image

        :param server_id: the uuid for the server to rescue
        :param rescue_id: optional uuid of the image to replace the rescued instance
                          with
        :param version: keystone authentication version (v2 or v3)
        :return:
        """
        ks = keystone.create_keystone(version=version)
        nova_url = ks.service_catalog.url_for(service_type="compute",
                                                   endpoint_type="publicURL")
        rescue_url = os.path.join(nova_url, "servers/{}/rescue".format(server_id))
        hdr = {"X-Auth-Token": ks.auth_token}
        print("Sending rescue api to url: {}".format(rescue_url))

        http = httplib2.Http()
        if rescue_id is not None:
            request = {"rescue": {"rescue_image_ref": rescue_id}}
            if admin_pw is not None:
                request["rescue"]["adminPass"] = admin_pw
            print("Request: {}".format(json.dumps(request)))
            return http.request(rescue_url, "POST", headers=hdr,
                                body=json.dumps(request))
        return http.request(rescue_url, "POST", headers=hdr)

    def filter_by(self, fn, sort_fn=None):
        """
        A helper function factory that takes a function that produces a sequence and
        optionally a sorting predicate function.  This sorting function takes 1 arg
        (an element from the sequence) and will include the element if the predicate
        returns a truthy value, otherwise it will not be included

        :param fn:
        :param sort_fn:
        :return:
        """

        def outer(*args, **kwargs):
            result = fn(*args, **kwargs)
            if sort_fn is None:
                return result
            else:
                return [x for x in result if sort_fn(x)]

        return outer

    def list_flavors(self, filt=None):
        seq = self.nova_session.flavors.list()
        if filt is None:
            return seq
        return [x for x in seq if filt(x)]

    def get_by_name(self, name):
        """
        A closure that can be used for filter_by
        :param name:
        :return:
        """
        return lambda x: name == x.name

    def get_by_id(self, id):
        return lambda x: id == x.id

    def list_instances(self, fn=None):
        """
        Returns a list of servers from the nova instance.

        Can take a filtering predicate function that takes an Server class instance
        as its sole argument.  For example:

        def filter_by_name(name, server):
            if name in server.name:
                return True
            return False

        fnc = partial(filter_by_name, "numa")
        servers = list_instances(nova, fnc)

        :param fn:
        :return:
        """
        if fn is None:
            return self.nova_session.servers.list()
        return [srv for srv in self.nova_session.servers.list() if fn(srv)]

    def list_hypervisors(self, fn=None):
        """
        Returns either a lazy sequence of hypervisors, or a filtered list of them

        :param fn: a filtering predicate function that takes a hypervisor object arg
        :return: a generator that walks the found hypervisors if no filtering
                 function, a list of filtered hypervisors otherwise
        """
        if fn is None:
            return self.nova_session.hypervisors.list()
        return [hv for hv in self.nova_session.hypervisors.list() if fn(hv)]

    def _poll_for_status(self, instance, status, poll_interval=2, timeout=300, log=False):
        """
        Polls for the status of a nova instance

        :param instance: The nova instance object to poll
        :param status: What status to check for.  If "deleted", polls until the
                       instance has been deleted
        :param poll_interval:
        :param timeout:
        :return:
        """
        start_time = time.time()

        def timer():
            endtime = start_time + timeout
            if timeout is None:
                return True
            else:
                timenow = time.time()
                check = endtime > timenow
                return check

        achieved = False
        while timer():
            try:
                instance.get()
            except NotFound as nf:
                if status == "deleted":
                    achieved = True
                    break
                else:
                    raise nf
            except AttributeError as ae:
                if status == "deleted":
                    achieved = True
                    break
                else:
                    raise ae
            else:
                if instance.status == "ERROR":
                    if status == "ERROR":
                        achieved = True
                    else:
                        glob_logger.error("Failed to boot instance")
                    break
                if instance.status != status:
                    if log:
                        msg = "Checking for {} on {}: status is {}"
                        msg = msg.format(status, instance.name, instance.status)
                        glob_logger.info(msg)
                    time.sleep(poll_interval)
                else:
                    achieved = True
                    break
        return achieved

    def poll_status(self, instance, status, block=True, poll_interval=3, timeout=300,
                    log=False):
        """
        Wrapper around _poll_for_status that can be used to either block until the
        desired state is achieved, or spin off the polling in a separate thread

        :param instance: A Server instance
        :param status: a string matching a possible nova instance status
                      (eg "ACTIVE"). If "deleted", poll until instance has been
                      deleted
        :param poll_interval: How often to poll the status
        :param timeout: In seconds, how long to wait until returning
        :return:
        """
        if block:
            return self._poll_for_status(instance, status, poll_interval=poll_interval,
                                         timeout=timeout, log=log)

    def server_group_create(self, name, policies="affinity"):
        """
        Creates an affinity or anti-affinity group

        :param name:
        :param policies: comma separated list of policies for the group
        :return:
        """
        policies = policies.split(",")
        body = {"name": name, "policies": policies}
        return self.nova_session.server_groups.create(**body)

    def server_group_list(self):
        """

        :return: list of groups.
        """
        return self.nova_session.server_groups.list()

    def create_flavor(self, name, ram, num_vcpus, disksize):
        """
        Creates a new nova Flavor object

        :param name: a name to give the new flavor (need not be unique)
        :param ram: amount of RAM in MB to give the flavor
        :param num_vcpus: the number of vcpus to allocate this flavor
        :param disksize: the disksize in GB
        :return:
        """
        return self.nova_session.flavors.create(name, ram, num_vcpus, disksize)

    def list_images(self):
        return self.nova_session.images.list()

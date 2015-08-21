__author__ = "Toure Dunnon, Sean Toner"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com, stoner@redhat.com"
__status__ ="Alpha"

"""
This module contains low-level functions surrounding libvirt, or directly
getting system information from a host
"""

import time
import libvirt
import re
import xml.etree.ElementTree as ET
from subprocess import PIPE
try:
    import untangle
except ImportError:
    print("Module untangle not available.")

from iridium.core.commander import Command, CommandException
import iridium.core.exceptions as sce
from iridium.core.logger import glob_logger


def get_connection(hv_ip, user="root", driver="qemu+ssh"):
    """
    Returns a connection ref to the hypervisor

    :param hv_ip: (str) hypervisor's ip address
    :param user: (str) user to connect as
    :return: libvirt Connection object
    """
    return libvirt.open("{}://{}@{}/system".format(driver, user, hv_ip))


def get_domain(master, vm_name, user="root", driver="qemu+ssh"):
    """
    Get a libvirt Domain object

    :param master: (str) ip address of the hypervisor
    :param vm_name: libvirt domain name
    :param user: user to log into libvirt as
    :return: libvirt Domain object
    """
    conn = get_connection(master, user=user, driver=driver)
    domain = conn.lookupByName(vm_name)
    return domain


def get_capabilities(conn):
    """
    Returns a string which is the XML of the hypervisor's capabilities

    :param conn: libvirt Connection object
    :return: (str) of capabilities in XML format
    """
    return conn.getCapabilities()


def make_capabilities_tree(xmlstr):
    xmldump = ET.fromstring(xmlstr)
    return xmldump


def get_cpu_cap(tree):
    cpu = tree.find("./host/cpu")
    return cpu


def get_topology_cap(tree):
    return tree.find("./host/topology")


def get_virt_type(dom):
    """
    Gets the xml dump for a domain and checks the <domain type=""> attribute
    :param dom: Domain object
    :return:
    """
    xmldump = dom.XMLDesc()

    # TODO: search the xml to get the virt_type


def rebooter(host, timeout=360):
    """
    Reboots a machine  and pings the host periodically until it is up

    :param host: IP address of machine to reboot
    :param timeout: timeout in seconds
    :return: None
    """
    res = Command("reboot", host=host)(throws=False)

    # Wait until pings are unsuccessful
    start_time = time.time()
    end_time = start_time + timeout
    while True:
        pinger = Command("ping -W 4 -c 4 {}".format(host), stderr=PIPE)
        result = pinger(showout=False, throws=False)
        if result != 0:
            break
        if time.time() > end_time:
            raise Exception("Machine did not reboot")


def pinger(host, timeout=300):
    """

    :param host: IP address of machine to ping to
    :param timeout: timeout in seconds
    :return: None
    """
    ping = Command("ping -W 4 -c 4 {}".format(host), stderr=PIPE)

    start_time = time.time()
    end_time = start_time + timeout
    while True:
        glob_logger.info("waiting for {} to come back up...".format(host))
        res = ping(showout=False, throws=False)
        if res == 0:
            glob_logger.info("{} is back up".format(host))
            break
        time.sleep(10)
        if time.time() > end_time:
            err = "Machine did not come back after {} seconds".format(timeout)
            raise Exception(err)


def verify_nested_kvm(host):
    """
    Goes through loaded modules to see if kvm_intel or kvm_amd is loaded

    :param host: (str) IP Address of host
    :return: The CPU type (str) intel or amd
    """
    glob_logger.info("Checking is kvm and kvm-intel or kvm-amd is running...")
    lsmod = Command("lsmod", host=host)(showout=False)
    patt = re.compile(r"kvm_(intel|amd)")

    out = lsmod.output

    for line in lsmod.output.split("\n")[1:]:
        m = patt.search(line)
        if m:
            proc = m.groups()[0]
            break
    else:
        raise sce.ConfigException("kvm module is not loaded")

    return proc


def verify_modprobe(host, proc_type="intel", set=False):
    """
    Checks if nested option is set for kvm_intel|amd, and optionally
    set it in /etc/modprobe.d/dist.conf

    :param host: (str) IP address of host
    :param proc_type: one of 'intel' or 'amd'
    :param set: (bool) chose to create dist.conf or not
    :return: ProcessResult of setting dist.conf or match from regex
    """
    line = "options kvm_{} nested=y".format(proc_type)

    def set_options(cfg):
        cmd = "echo {} >> /etc/modprobe.d/dist.conf".format(cfg)
        res = Command(cmd, host=host)(showout=False)
        return res == 0

    # /etc/modprobe.d/dist.conf may not exist
    try:
        res = Command("cat /etc/modprobe.d/dist.conf", host=host)(showout=False)
    except CommandException:
        r = False
        if set:
            r = set_options(line)
        return r
    else:
        patt = re.compile(line)
        m = patt.search(res.output)
        if not set or (set and m):
            return m

        return set_options(line)


def set_host_passthrough(hyper_ip, dom_name, user="root"):
    """
    Sets a domain's <cpu> element to use mode host-passthrough

    :param hyper_ip: (str) IP address of host with hypervisor
    :param dom_name: (str) the libvirt domain name
    :param user: (str) user to connect to libvirt hypervisor
    :return: ProcessTresult
    """
    # FIXME: How do we do this just using libvirt?  This adds a dependency
    # on virt-xml
    # Edit the domain's xml to use host-passthrough mode
    glob_logger.info("Setting host-passthrough mode for {}".format(dom_name))
    cmd = "virt-xml --connect=qemu+ssh://{}@{}/system {} --edit --cpu " \
          "host-passthrough,clearxml=yes".format(user, hyper_ip, dom_name)
    res = Command(cmd)()
    return res


def get_host_model(hyper_ip, dom_name, user="root", driver="qemu+ssh"):
    """

    :param hyper_ip: IP Address of hypervisor
    :param user: user to connect to libvirt
    :param driver: the libvirt driver to connect with
    :return: the attribute of the domain <cpu> element
    """
    dom = get_domain(hyper_ip, dom_name, user=user, driver=driver)
    dump = dom.XMLDesc()
    xmldom = untangle.parse(dump)
    return xmldom.domain.cpu["mode"]


def set_host_model(hyper_ip, dom_name, user="root"):
    """
    Can be used as fn arg to set_nested_vm_support

    :param hyper_ip: the IP address of hypervisor machine
    :param dom_name: the libvirt domain name
    :param user: user to connect to libvirt as
    :return: ProcessResult of executing virt-xml command
    """
    glob_logger.info("Setting host_model mode for {}".format(dom_name))
    cmd = "virt-xml --connect=qemu+ssh://{}@{}/system {} --edit --cpu " \
          "host-model-only,+vmx"
    cmd = cmd.format(user, hyper_ip, dom_name)
    return Command(cmd)()


def test_and_set_kvm_module(bare_m):
    """
    Checks if kvm_intel|amd is loaded.  if not will try to modprobe it

    :param bare_m: address of baremetal machine
    :return: (str) cpu type intel or amd
    """
    p = verify_nested_kvm(bare_m)
    if p is None:
        # kvm is not loaded
        Command("modprobe kvm", host=bare_m)()
        p = verify_nested_kvm(bare_m)
        if p is None:
            raise sce.ConfigException("Can not load kvm module")
    return p


def test_and_set_distconf(bare_m, cpu):
    """
    Checks if kvm module is set to boot up in dist.conf to make it persistent
    after a reboot

    :param bare_m:
    :param cpu:
    :return:
    """
    hosts = [bare_m]
    for h in hosts:
        m = verify_modprobe(h, proc_type=cpu, set=False)
        if not m:
            verify_modprobe(h, proc_type=cpu, set=True)
            m = verify_modprobe(h, proc_type=cpu)
            if m is False or m is None:
                raise sce.ConfigException("Could not set /etc/modprobe.d/dist.conf")


def turn_on(hv_ip, domain_name, ip_addr, wait=5):
    """
    Powers on a VM given the hypervisor IP address and VM's domain name

    :param bare_metal:
    :param domain_name:
    :param ip_addr:
    :return:
    """
    dom_ = get_domain(hv_ip, domain_name)
    if dom_.state()[0] not in [1]:
        # Start the L1 guest hypervisor
        glob_logger.info("Bringing back up L1 hypervisor {}".format(ip_addr))
        power_on(dom_)
        time.sleep(1)
        pinger(ip_addr)
        time.sleep(wait)  # Give a few seconds for services to come up
    return dom_


def test_and_set_nested(host, timeout=600):
    """
    Verifies that the host has nested virtualization set for kvm module

    :param host:
    :param timeout:
    :return: ProcessResult
    """
    cmd = "cat /sys/module/kvm_intel/parameters/nested"
    res = Command(cmd, host=host)(showout=False)
    if res.output.strip() != "Y":
        # Reboot the masters machine
        glob_logger.info("rebooting {} to set nested param".format(host))
        rebooter(host, timeout=timeout)
        time.sleep(45)    # Fudge factor here...
        pinger(host, timeout=timeout)

        # After reboot, make sure nested support is there
        path = "/sys/module/kvm_intel/parameters/nested"
        cmd = "cat {}".format(path)
        try:
            res = Command(cmd, host=host)(showout=False)
            if res.output.strip() != "Y":
                glob_logger.error("{}={}".format(path, res.output.strip()))
                raise sce.ConfigException("Nested support still not enabled")
        except CommandException:
            raise sce.ConfigException("Nested support still not enabled")
    return res


def check_kvm_file(host):
    """
    Checks of the /dev/kvm special file exists on host

    :param host: (str) IP address of machine
    :return: ProcessResult object (or throws ConfigException)
    """
    glob_logger.info("Checking /dev/kvm")
    res = Command("file /dev/kvm", host=host)()
    if "cannot open" in res.output:
        raise sce.ConfigException("no /dev/kvm on {}".format(host))
    return res


def set_nested_vm_support(bare_m, dom_info, fn=set_host_passthrough, kvm=True,
                          user="root", timeout=600):
    """
    Sets nested support for the masters and any domains.

    This works by enabling KVM extensions on the baremetal host, and also
    setting the correct domain xml on the L1 hypervisors.

    :param bare_m: (str) ip address of the masters machine
    :param dom_info: a tuple of (ip, domain_name) for L1 guests
    :param fn: a function that takes the masters IP, a domain name, and user
    :param kvm: (bool) check to see if /dev/kvm exists
    :param user:
    :return:
    """
    msg = "Verifying and setting nested VM support on {}..."
    glob_logger.info(msg.format(dom_info))

    # Make sure that the L1 guests are running
    ip, dom_name = dom_info
    dom_ = get_domain(bare_m, dom_name)
    glob_logger.info("Making sure {} is running".format(dom_name))
    state = dom_.state()
    if state[0] not in [1]:
        glob_logger.info("Powering up {}".format(dom_name))
        power_on(dom_)

    # Make sure kvm module is loaded
    cpu = test_and_set_kvm_module(bare_m)

    # Make sure /etc/modprobe.d/dist.conf is set
    glob_logger.info("Verifying if /etc/modprobe.d/dist.conf is set")
    test_and_set_distconf(bare_m, cpu)

    # We only need to do this if our domain isn't already set for host
    # passthrough mode.  So let's check it first
    root = ET.fromstring(dom_.XMLDesc())
    cpu = list(root.iter("cpu"))[0]
    cpu_mode = fn.__name__ == "set_host_passthrough" or \
               fn.__name__ == "set_host_model"
    mode_type = fn.__name__ if fn else None

    # Check to see if we already have the mode setup
    info = untangle.parse(dom_.XMLDesc())
    passthrough_set = False
    host_model_set = False

    if info.domain.cpu["mode"] == "host-passthrough":
        passthrough_set = True
    elif info.domain.cpu["mode"] == "custom":
        host_model_set = True

    # Make sure that the L1 hypervisor is shutdown before taking down bare_m
    already_set = False
    if fn is not None and cpu_mode:
        if (mode_type == "set_host_passthrough" and passthrough_set) or \
                (mode_type == "set_host_model" and host_model_set):
            already_set = True
        else:
            glob_logger.info("Taking down L1 hypervisor {}".format(ip))
            state = dom_.state()
            if state[0] in [1]:
                shutdown(dom_)

    # Check if the masters has nested support after reboot
    _ = test_and_set_nested(bare_m)

    # If we aren't doing host passthrough, we're done
    if fn is None or already_set:
        turn_on(bare_m, dom_name, ip)
        pinger(ip)
        return

    # Otherwise, call our passthrough function if we dont already have
    # passthrough mode enabled
    if cpu_mode:
        glob_logger.info("calling {}".format(fn.__name__))
        fn(bare_m, dom_name, user=user)

    turn_on(bare_m, dom_name, ip)
    pinger(ip)
    time.sleep(10)   # TODO: uggh, need to know when SSH is up

    # Make sure we have the /dev/kvm special file
    if kvm:
        check_kvm_file(ip)


def shutdown(domain, timeout=120):
    """
    Shutdown the hosts that the instance lives on

    :param domain: libvirt domain object
    :param timeout:
    :return: int domain state
    """
    domain.destroy()
    start_time = time.time()
    end_time = start_time + timeout  # timeout in 2 min
    while True:
        state = domain.state()[0]
        if state == libvirt.VIR_DOMAIN_SHUTOFF:
            break
        if end_time < time.time():
            break
    return domain.state()[0]


def power_on(domain, timeout=30):
    """
    Powers on a VM

    :param domain: libvirt domain object
    :param timeout: timeout in seconds
    :return: int domain state
    """
    domain.create()
    start_time = time.time()
    end_time = start_time + timeout
    while True:
        state = domain.state()[0]
        if state == libvirt.VIR_DOMAIN_RUNNING:
            break
        if time.time() > end_time:
            break
    else:
        raise Exception("Could not power back on the compute node")
    return domain.state()[0]


def get_devices(conn, dtype="pci"):
    """
    Return a lazy sequence of NodeDevice objects

    :param conn:
    :param dtype:
    :return:
    """
    for pcid in conn.listDevices(dtype):
        yield conn.nodeDeviceLookupByName(pcid)


def get_cpu_topology(conn):
    """
    Parses the virsh capabilities from a libvirt connection object
    and returns a dictionary describing the CPU topology.

    This can be used to determine how many NUMA nodes there are, and
    how many CPUs there are for each numa cell

    :param conn: libvirt Connection object (from get_connection)
    :return: a list of dictionary describing the <cpu>
    """
    caps = get_capabilities(conn)
    root = ET.fromstring(caps)
    topo = root.iter("topology")

    cells = []
    cell = {}
    cell_id = None
    for item in topo:
        for child in item.iter():
            tag, attrib, text = child.tag, child.attrib, child.text
            if text:
                text = text.strip()
            if attrib is None:
                continue
            if tag == "cell":
                cell_id = attrib["id"]
                cell[cell_id] = {}
                cells.append(cell)
            if cell:
                if tag in cell[cell_id]:
                    if attrib or text:
                        cell[cell_id][tag].append({"attrib": attrib, "val": text})
                else:
                    cell[cell_id][tag] = []
                    if attrib or text:
                        cell[cell_id][tag].append({"attrib": attrib, "val": text})
    return cells


def friendly_topology(cells):
    """
    The structure returned from get_cpu_topology is not terribly friendly.
    So this function is more human readable.  It takes the cells output from
    get_cpu_topology, and converts it to a more human readable dictionary

    :param cells:
    :return:
    """
    info = {"num_numa_nodes": len(cells)}
    for item in cells:
        for id_, cell in item.items():
            cell_id = int(id_)
            info[cell_id] = {}
            for page in cell["pages"]:
                if page["attrib"]["size"] == "4":
                    info[cell_id]["pages"] = page["val"]
                else:
                    info[cell_id]["pages_large"] = page["val"]
            info[cell_id]["memory"] = cell["memory"][0]["val"]
            info[cell_id]["cpus"] = cell["cpus"][0]["attrib"]["num"]
    return info


if __name__ == "__main__":
    #import smog.virt as sv
    dom = ("10.8.30.113", "rhel71")
    bm = "10.8.0.58"
    set_nested_vm_support(bm, [dom], kvm=True)
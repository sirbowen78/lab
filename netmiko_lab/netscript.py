from pymongo import MongoClient
from netmiko import ConnectHandler
from functools import wraps
from jinja2 import Environment, FileSystemLoader
from ipaddress import IPv4Network

def mongodb_table(mongo_addr, dbname, tablename):
    client = MongoClient(mongo_addr)
    return client[dbname][tablename]


def config_template(template_path="templates", template_file=None):
    loader = FileSystemLoader(template_path)
    return Environment(loader=loader).get_template(template_file)


# Reference on how to do decorator on class instance methods.
def show(fn):
    """
    This decorator ensure enable mode before fn, and disconnect after fn.
    :param fn: function which has at least self as argument.
    :return: output of fn, and the wrapper.
    """
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not self.session.check_enable_mode():
            self.session.enable()
        output = fn(self, *args, **kwargs)
        self.session.disconnect()
        return output

    return wrapper


def config(fn):
    """
    This is a decorator ensure enable mode before fn, and execute save_config and disconnect
    after fn is executed.
    :param fn: function to execute, has at least class instance as argument (self), can accept
    positional arguments (*args) and keyword args (**kwargs)
    :return: output of fn, and the wrapper function so that the result is return
    and not eaten by decorator.
    """
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not self.session.check_enable_mode():
            self.session.enable()
        output = fn(self, *args, **kwargs)
        self.session.save_config()
        self.session.disconnect()
        return output

    return wrapper


def inverse_mask(netmask):
    """
    Cisco ACL uses inverse mask instead of actual subnet mask, this function is to
    invert the subnet mask.
    :param netmask: actual subnet mask such as 255.255.255.240
    :return: inverse mask
    """
    conversion = [str(255 - int(octet)) for octet in netmask.split(".")]
    return ".".join(conversion)


def cidr_to_netmask(subnet):
    """
    This function converts the /cidr to proper netmask.
    Reference: https://gist.github.com/nboubakr/4344773
    Manual method:
    mask = [0, 0, 0, 0]
    net_id, cidr = subnet.split("/")
    for i in range(int(cidr)):
        mask[i//8] = mask[i//8] + (1 << (7 - i % 8))
    netmask = [str(i) for i in mask]
    return net_id, ".".join(netmask)
    This manual method is good for cidr to netmask but there is no checks if the net_id within
    the network bound by cidr.

    By using ipaddress module is the easiest and recommended,
    because ipaddress.IPv4Network checks if the network id is a valid id
    within the range of its cidr.
    :param subnet: must be a subnet/cidr eg. 192.168.1.0/26
    :return: tuple of network id and netmask
    """
    _subnet = IPv4Network(subnet)
    return str(_subnet.network_address), str(_subnet.netmask)


def netmask_to_cidr(netmask):
    """
    This function converts netmask to cidr representation.
    1st step split the mask octet into a list, eg. 255.255.255.240 will be [255, 255, 255, 240]
    2nd step for each element in the list get the bin(), then count the occurrence of 1.
    eg. bin(255) = 8 (1s), bin(240) = 4 (1s) hence [8, 8, 8, 4]
    Final step add all numbers in the list, eg. [8, 8, 8, 4] = 28
    :param netmask: eg. 255.255.255.240
    :return: string of cidr eg. 28
    """
    mask_list = [str(bin(int(octet))).count("1") for octet in netmask.split(".")]
    return sum(mask_list)


class CiscoIOS:
    def __init__(self, ip="192.168.1.1", username="admin", password="password", secret=None):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        device = dict(
            device_type="cisco_ios",
            ip=self.ip,
            username=self.username,
            password=self.password,
        )
        if secret is not None:
            device.update(dict(secret=self.secret))
        self.session = ConnectHandler(**device)

    @show
    def show_intf_brief(self):
        return self.session.send_command("show ip int brief", use_textfsm=True)

    @show
    def show_version(self):
        return self.session.send_command("show version")

    @config
    def set_hostname(self, hostname):
        return self.session.send_config_set([f"hostname {hostname}"])

    @config
    def set_intf(self, **intf_config):
        template = config_template(template_file="intf.j2")
        config = template.render(**intf_config)
        return self.session.send_config_set([cmd.strip(" ") for cmd in config.splitlines()])

    @config
    def remove_loopback(self, loop_id=0):
        return self.session.send_config_set([f"no interface loopback{loop_id}"])

    @config
    def set_ospf(self, **ospf_config):
        template = config_template(template_file="ospf.j2")
        config = template.render(**ospf_config)
        return self.session.send_config_set(config.splitlines())


r1 = CiscoIOS(ip="192.168.1.209", username="cyruslab", password="cisco123", secret="cisco123")
r2 = CiscoIOS(ip="192.168.1.229", username="cyruslab", password="cisco123", secret="cisco123")
r1_ospf = dict(
    process_id=1,
    router_id="1.1.1.1",
    intf_id="Ethernet0/0",
    ipv4_addr="10.0.0.1",
    netmask="255.255.255.252",
    lo_id=1,
    area_id=0
)
r2_ospf = dict(
    process_id=1,
    router_id="2.2.2.2",
    intf_id="Ethernet0/0",
    ipv4_addr="10.0.0.2",
    netmask="255.255.255.252",
    lo_id=2,
    area_id=0
)

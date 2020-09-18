from pymongo import MongoClient
from netmiko import ConnectHandler
from functools import wraps
from jinja2 import Environment, FileSystemLoader
from ipaddress import IPv4Network


def mongodb_table(mongo_addr, dbname, tablename):
    """
    Get the db cursor
    :param mongo_addr: eg. mongdb://192.168.1.245:27017
    :param dbname: database name
    :param tablename: collection name
    :return: mongodb collection object
    """
    client = MongoClient(mongo_addr)
    return client[dbname][tablename]


def mongodb_insert_many(db_cursor, data_list):
    """
    Insert many rows in collection/table
    :param db_cursor: mongodb collection object
    :param data_list: list of dictionary data.
    :return:
    """
    db_cursor.insert_many(data_list)


def mongdb_find_one(db_cursor, filter, exclude):
    """
    Return the first found data from mongodb.
    :param db_cursor:
    :param filter: must be dictionary like eg. {"hostname": "r1"}
    :param exclude: must be dictionary like eg. {"_id": 0, "hostname": 0}
    :return: data
    """
    return db_cursor.find_one(filter, exclude)


def config_template(template_path="templates", template_file=None):
    loader = FileSystemLoader(template_path)
    return Environment(loader=loader).get_template(template_file)


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
    return sum([str(bin(int(octet))).count("1") for octet in netmask.split(".")])


class CiscoIOS:
    """
    Only for Cisco IOS XE.
    """

    def __init__(self, ip="192.168.1.1", username="admin", password="password", secret=None):
        """
        information for netmiko to connect to cisco ios based router.
        :param ip: management ip address of router
        :param username: username of router
        :param password: password of router
        :param secret: optional, this is the enable password of router.
        """
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
        """
        show router interface summary.
        :return: command line output
        """
        return self.session.send_command("show ip int brief", use_textfsm=True)

    @show
    def show_version(self):
        return self.session.send_command("show version")

    @config
    def set_hostname(self, hostname):
        """
        Modify hostname of router.
        :param hostname: desired name for the router
        :return: command line output
        """
        return self.session.send_config_set([f"hostname {hostname}"])

    @config
    def set_intf(self, **intf_config):
        template = config_template(template_file="intf.j2")
        config = template.render(**intf_config)
        return self.session.send_config_set([cmd.strip(" ") for cmd in config.splitlines()])

    @config
    def remove_loopback(self, loop_id=0):
        """
        Remove loopback interface
        :param loop_id: the loopback interface id to remove.
        :return: command line output
        """
        return self.session.send_config_set([f"no interface loopback{loop_id}"])

    @config
    def set_ospf(self, **ospf_config):
        """
        Configures the ospf.
        :param ospf_config: ospf configuration data
        :return: command line output
        """
        template = config_template(template_file="ospf.j2")
        config = template.render(**ospf_config)
        return self.session.send_config_set(config.splitlines())

    @config
    def acl_insert_one(self, **extended_acl_config):
        """
        Insert one entry to extended acl.
        :param extended_acl_config:
        :return: command line output
        """
        template = config_template(template_file="named_acl_extended.j2")
        config = template.render(**extended_acl_config)
        return self.session.send_config_set(config.splitlines())

    @config
    def apply_acl(self, **apply_acl):
        """
        This is to apply acl in interface.
        :param apply_acl:
        :return: command line ouput
        """
        template = config_template(template_file="apply_acl.j2")
        config = template.render(**apply_acl)
        return self.session.send_config_set(config.splitlines())

    @config
    def default_intf(self, intf_id):
        """
        Reset interface to default.
        :param intf_id:
        :return: command line output
        """
        return self.session.send_config_set([f"default interface {intf_id}"])

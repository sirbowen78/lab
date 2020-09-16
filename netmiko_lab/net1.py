from netmiko import ConnectHandler
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader


def init_j2_template(template_dir):
    """
    Initialize jinja2 template
    :param template_dir: j2 template location
    :return: Environment object
    """
    file_loader = FileSystemLoader(template_dir)
    return Environment(loader=file_loader)


def get_device_config(mongo_url="mongodb://192.168.1.245:27017",
                      dbname="testdb",
                      table_name="testtbl",
                      ip="127.0.0.1"):
    """
    Get cisco router's device config suitable for consumption by netmiko.ConnectHandler
    :param mongo_url:
    :param dbname:
    :param table_name:
    :param ip:
    :return:
    """
    client = MongoClient(mongo_url)
    return client[dbname][table_name].find_one({"ip": ip}, {"_id": 0})


def config_ospf(netmiko_connector, j2env, **ospf_config):
    """
    Use the ospf.j2 template, fill up the ospf_config info,
    and send the configuration set.
    :param netmiko_connector:
    :param j2env:
    :param ospf_config:
    :return:
    """
    template = j2env.get_template("ospf.j2")
    config = template.render(**ospf_config)
    # netmiko.send_config_set requires configuration to be sent as a list of command lines.
    # otherwise netmiko will throw timeout exception despite command lines sent.
    return netmiko_connector.send_config_set(config.splitlines())


def config_intf(netmiko_connector, j2env, **intf_config):
    template = j2env.get_template("intf.j2")
    config = template.render(**intf_config)
    return netmiko_connector.send_config_set([cmd.strip(' ') for cmd in config.splitlines()])


def enable_mode(netmiko_connector):
    # required to use netmiko.send_config_set
    if not netmiko_connector.check_enable_mode():
        netmiko_connector.enable()


def config_router(device_config, config_what=None, **router_config):
    """
    :param config_what:
    :param device_config:
    :param router_config:
    :return:
    """
    with ConnectHandler(**device_config) as conn:
        env = init_j2_template("templates")
        enable_mode(conn)
        if config_what.lower() == "ospf":
            print(config_ospf(conn, env, **router_config))
        elif config_what.lower() == "intf":
            print(config_intf(conn, env, **router_config))
        conn.save_config()


def update_router_interface_status(mongodb_table, interface_result):
    """
    This updates the interface status table, the _id and intf columns do not change.
    This function is to update the ipaddr, status and proto columns.
    The function compares mongodb_table and result of interface_result, if mongodb_table
    differs from interface_result then updates the mongodb_table.
    :param mongodb_table:
    :param interface_result:
    :return:
    """
    for db_row in mongodb_table.find({}, {"_id": 0}):
        for row in interface_result:
            if db_row["ipaddr"] != row["ipaddr"]:
                mongodb_table.update_one({"intf": row["intf"]}, {"$set": {"ipaddr": row["ipaddr"]}})
            if db_row["status"] != row["status"]:
                mongodb_table.update_one({"intf": row["intf"]}, {"$set": {"status": row["status"]}})
            if db_row["proto"] != row["proto"]:
                mongodb_table.update_one({"intf": row["intf"]}, {"$set": {"proto": row["proto"]}})


def refresh_collection(collection, interface_result):
    """
    This function refresh the collection, by dropping existing collection.
    if collection is new it is created in the collection argument, the documents
    are inserted anyway. The drop method will not throw exception even if the
    collection does not exist.
    This is very straight forward drop the table and insert updated on from router.
    :param collection:
    :param interface_result:
    :return:
    """
    collection.drop()
    collection.insert_many(interface_result)


def get_interface_brief(**device_config):
    with ConnectHandler(**device_config) as conn:
        result = conn.send_command("show ip int brief", use_textfsm=True)
    return result


if __name__ == "__main__":
    r1_device_config = get_device_config(dbname="network", table_name="devices", ip="192.168.1.215")

    r2_device_config = get_device_config(dbname="network", table_name="devices", ip="192.168.1.232")

    r1_ospf_config = dict(
        process_id=1,
        router_id="1.1.1.1",
        intf_id="Ethernet0/0",
        ipv4_addr="10.0.0.1",
        netmask="255.255.255.252",
        area_id=0,
        lo_id=1
    )

    r2_ospf_config = dict(
        process_id=1,
        router_id="2.2.2.2",
        intf_id="Ethernet0/0",
        ipv4_addr="10.0.0.2",
        netmask="255.255.255.252",
        area_id=0,
        lo_id=2
    )

    intf_config = {
        "intf_id": "Ethernet0/3",
        #"desc": "This is a test description",
        "ipaddr": "",
        #"netmask": "255.255.255.0",
        "up": False
    }

    r1_result = get_interface_brief(**r1_device_config)
    client = MongoClient("mongodb://192.168.1.245:27017")

    r1_table = client["network"]["R1"]
    refresh_collection(r1_table, r1_result)

    r2_result = get_interface_brief(**r2_device_config)
    r2_table = client["network"]["R2"]
    refresh_collection(r2_table, r2_result)

    config_router(r1_device_config, config_what="intf", **intf_config)

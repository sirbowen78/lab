from netmiko import ConnectHandler
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader


def init_j2_template(template_dir):
    file_loader = FileSystemLoader(template_dir)
    return Environment(loader=file_loader)


def get_device_config(mongo_url="mongodb://192.168.1.245:27017",
                      dbname="testdb",
                      table_name="testtbl",
                      ip="127.0.0.1"):
    client = MongoClient(mongo_url)
    return client[dbname][table_name].find_one({"ip": ip}, {"_id": 0})


def config_ospf(netmiko_connector, j2env, **ospf_config):
    template = j2env.get_template("ospf.j2")
    config = template.render(**ospf_config)
    return netmiko_connector.send_config_set(config.splitlines())


def enable_mode(netmiko_connector):
    if not netmiko_connector.check_enable_mode():
        netmiko_connector.enable()


if __name__ == "__main__":
    r1_device_config = get_device_config(dbname="network", table_name="devices", ip="192.168.1.215")
    r1_device_config.update(
        dict(
            secret=r1_device_config["password"]
        )
    )

    r2_device_config = get_device_config(dbname="network", table_name="devices", ip="192.168.1.232")
    r2_device_config.update(
        dict(
            secret=r2_device_config["password"]
        )
    )

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

    with ConnectHandler(**r1_device_config) as r1:
        env = init_j2_template("templates")
        enable_mode(r1)
        print(config_ospf(r1, env, **r1_ospf_config))
        r1.save_config()

    with ConnectHandler(**r2_device_config) as r2:
        env = init_j2_template("templates")
        enable_mode(r2)
        print(config_ospf(r2, env, **r2_ospf_config))
        r2.save_config()

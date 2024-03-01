from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Host,
    Tag,
    PortFB,
    Port,
    AuditLog,
    Statistics,
    DiscoveredDevice,
    HostTag,
)
import random
import os

# Get the absolute directory path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the database directory relative to the script location
database_dir = os.path.join(script_dir, "database")

# Ensure the database directory exists
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

# Construct the database URI
DATABASE_URI = "sqlite:///" + os.path.join(database_dir, "ip_atlas.db")
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

fake = Faker()


def generate_test_data(
    num_hosts=50, num_logs=10, num_stats=5, num_devices=20, num_ports_per_host=2
):
    session = Session()
    # Generate Hosts, Tags, PortFBs, and Ports
    for i in range(1, num_hosts + 1):
        hostname = f"Host{i}"
        ipv4 = fake.ipv4_private(network=False, address_class=None)
        ipv6 = fake.ipv6(network=False)

        host = Host(hostname=hostname, ipv4=ipv4, ipv6=ipv6, deleted=fake.boolean())
        session.add(host)
        session.commit()  # Commit to assign an ID to the host

        for _ in range(num_ports_per_host):
            portFB_number = fake.random_int(min=1, max=65535)
            portFB = PortFB(host_id=host.id, portFB_number=portFB_number)
            session.add(portFB)

            port_number = fake.random_int(min=1, max=65535)
            port = Port(host_id=host.id, port_number=port_number)
            session.add(port)

        tags = [fake.word(), fake.word(), "test"]
        for tag_name in tags:
            tag = session.query(Tag).filter_by(tag_name=tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name, deleted=fake.boolean())
                session.add(tag)
                session.commit()

            host_tag = HostTag(host_id=host.id, tag_id=tag.id)
            session.add(host_tag)

    # Generate AuditLogs
    for _ in range(num_logs):
        audit_log = AuditLog(
            action_type=fake.word(),
            table_name=fake.word(),
            record_id=fake.random_int(min=1, max=100),
            user=fake.name(),
            timestamp=fake.date_time_this_decade(),
        )
        session.add(audit_log)

    # Generate Statistics
    for _ in range(num_stats):
        stat = Statistics(
            stat_key=fake.word(),
            stat_value=fake.random_int(min=1, max=1000),
            last_updated=fake.date_time_this_decade(),
        )
        session.add(stat)

    # Generate DiscoveredDevices
    for _ in range(num_devices):
        device = DiscoveredDevice(
            mac_address=fake.mac_address(),
            ipv4=fake.ipv4(),
            ipv6=fake.ipv6(),
            hostname=fake.hostname(),
            first_seen=fake.date_time_this_decade(),
            last_seen=fake.date_time_this_decade(),
            blacklist=fake.boolean(),
            used=fake.boolean(),
            vendor=fake.company(),
        )
        session.add(device)

    session.commit()


generate_test_data()

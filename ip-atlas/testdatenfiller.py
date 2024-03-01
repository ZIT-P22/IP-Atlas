from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    db,
    Host,
    Tag,
    PortFB,
    AuditLog,
    Statistics,
    DiscoveredDevice,
    HostTag,
)
import random
from app import atlasapp
import os

# Assuming your database URI is stored in a variable or directly provided
database_dir = os.path.join(os.getcwd(), "database")
DATABASE_URI = "sqlite:///" + os.path.join(database_dir, "ip_atlas.db")
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

fake = Faker()


def generate_test_data(num_hosts=50, num_logs=10, num_stats=5, num_devices=20):
    session = Session()
    # Generate Hosts, Tags, and PortFBs
    for i in range(1, num_hosts + 1):
        hostname = f"Host{i}"
        ipv4 = fake.ipv4_private(network=False, address_class=None)
        ipv6 = fake.ipv6(network=False)
        portsFB_numbers = [fake.random_int(min=1, max=65535) for _ in range(2)]

        host = Host(hostname=hostname, ipv4=ipv4, ipv6=ipv6)
        session.add(host)
        session.commit()  # Commit to assign an ID to the host

        for portFB_number in portsFB_numbers:
            portFB = PortFB(host_id=host.id, portFB_number=portFB_number)
            session.add(portFB)

        tags = [fake.word(), fake.word(), "test"]
        for tag_name in tags:
            tag = session.query(Tag).filter_by(tag_name=tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name)
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
        )
        session.add(audit_log)

    # Generate Statistics
    for _ in range(num_stats):
        stat = Statistics(
            stat_key=fake.word(), stat_value=fake.random_int(min=1, max=1000)
        )
        session.add(stat)

    # Generate DiscoveredDevices
    for _ in range(num_devices):
        device = DiscoveredDevice(
            mac_address=fake.mac_address(),
            ipv4=fake.ipv4(),
            ipv6=fake.ipv6(),
            hostname=fake.hostname(),
            vendor=fake.company(),
        )
        session.add(device)

    session.commit()


generate_test_data()

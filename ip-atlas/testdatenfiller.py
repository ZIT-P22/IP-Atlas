from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Host, Tag, Port, HostTag, PortFB
import random
from app import atlasapp
import os

# Assuming your database URI is stored in a variable or directly provided
database_dir = os.path.join(os.getcwd(), "database")
DATABASE_URI = "sqlite:///" + os.path.join(database_dir, "ip_atlas.db")
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

fake = Faker()


def generate_test_data(num_hosts=50):
    session = Session()
    for i in range(1, num_hosts + 1):
        hostname = f"Host{i}"
        ipv4 = fake.ipv4_private(network=False, address_class=None)
        ipv6 = fake.ipv6(network=False)
        # ports_numbers = [fake.random_int(min=1, max=65535) for _ in range(2)]
        portsFB_numbers = [fake.random_int(min=1, max=65535) for _ in range(2)]

        # Create Host instance
        host = Host(hostname=hostname, ipv4=ipv4, ipv6=ipv6)
        session.add(host)
        session.commit()  # Commit to assign an ID to the host

        # Create Port instances
        # for port_number in ports_numbers:
        #     port = Port(host_id=host.id, port_number=port_number)
        #     session.add(port)

        # Create PortFB instances
        for portFB_number in portsFB_numbers:
            portFB = PortFB(host_id=host.id, portFB_number=portFB_number)
            session.add(portFB)

        # Create and associate Tags
        tags = [fake.word(), fake.word(), "test"]
        for tag_name in tags:
            tag = session.query(Tag).filter_by(tag_name=tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name)
                session.add(tag)
                session.commit()  # Commit to assign an ID to the tag

            # Create association between host and tag
            host_tag = HostTag(host_id=host.id, tag_id=tag.id)
            session.add(host_tag)

        session.commit()


generate_test_data()

# host  = Host.query.filter_by(id=1).first()
# print(host.hostname)
# host.hostname = "test"
# db.session.commit()
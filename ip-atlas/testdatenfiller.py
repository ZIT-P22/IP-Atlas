from helper import writeJson
from faker import Faker

fake = Faker()


def generate_test_data(num_hosts=50):
    for i in range(1, num_hosts + 1):
        hostname = f"Host{i}"
        ipv4 = fake.ipv4_private(network=False, address_class=None)
        tags = [fake.word(), fake.word(), "test"]
        ipv6 = fake.ipv6(network=False)
        ports = [fake.random_int(min=1, max=65535) for _ in range(2)]
        writeJson(hostname, ipv4, tags, ipv6, ports)


generate_test_data()

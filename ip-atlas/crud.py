# this Script contains the CRUD operations for the ip-atlas database
# Author: Janneck Lehmann
# Date: 2024-02-07
from models import Host, Port, Tag


# function which reads all hosts from the database where the attribute deleted is set to false
def read_all_hosts():
    hosts = Host.query.filter_by(deleted=False).all()
    return hosts

# hosts = Host.query.all()
#     data = {"hosts": []}
#     for host in hosts:
#         host_data = {
#             "id": host.id,
#             "name": host.hostname,
#             "ip": host.ipv4,  # Assuming ipv4 is the primary IP to display
#             "ports": [port.port_number for port in host.ports],
#             "tags": [host_tag.tag.tag_name for host_tag in host.tags],  # Adjusted line
#         }
#         data["hosts"].append(host_data)

# this Script contains the CRUD operations for the ip-atlas database
# Author: Janneck Lehmann
# Date: 2024-02-07
from models import db, Host, Tag, Port, HostTag, PortFB
from helper import *



# function which converts the given data from db to the json format
def convert_to_json_format(host):
    host_data = {
        "id": host.id,
        "name": host.hostname,
        "ip": host.ipv4,
        "ipv6": host.ipv6,  
        "portsFB": [portFB.portFB_number for portFB in host.portsFB],
        "tags": [host_tag.tag.tag_name for host_tag in host.tags],
    }
    return host_data

# function which reads the host from the database by the given id
def get_host_by_id(id):
    host = Host.query.filter_by(id=id).first()
    return convert_to_json_format(host)

#

# function which reads all hosts from the database where the attribute deleted is set to false
def read_all_hosts():
    hosts = Host.query.filter_by(deleted=False).all()
    return hosts

# function which writes the given data to the database
def write_to_db(db, data):
    if db == "host":
        host = Host(hostname=data["name"], ipv4=data["ipv4"], ipv6=data["ipv6"])
        db.session.add(host)
    elif db == "port":
        port = Port(host_id=data["host_id"], port_number=data["port_number"])
        db.session.add(port)
    elif db == "tag":
        tag = Tag(tag_name=data["tag_name"])
        db.session.add(tag)
    elif db == "host_tag":
        host_tag = HostTag(host_id=data["host_id"], tag_id=data["tag_id"])
        db.session.add(host_tag)
    elif db == "portFB":
        portFB = PortFB(host_id=data["host_id"], portFB_number=data["portFB_number"])
        db.session.add(portFB)
    else:
        print("Error: Database not found")
    

# function which deletes the given data from the database
def delete_from_db(db, id):
    if db == "host":
        host = Host.query.filter_by(id=id).first()
        host.deleted = True
    elif db == "port":
        port = Port.query.filter_by(id=id).first()
        db.session.delete(port)
    elif db == "tag":
        tag = Tag.query.filter_by(id=id).first()
        tag.deleted = True
    elif db == "host_tag":
        host_tag = HostTag.query.filter_by(id=id).first()
        db.session.delete(host_tag)
    elif db == "portFB":
        portFB = PortFB.query.filter_by(id=id).first()
        db.session.delete(portFB)
    else:
        print("Error: Database not found")


# function which updates the given data in the database
def edit_db(db, data):
    if db == "host":
        host = Host.query.filter_by(id=data["id"]).first()
        host.hostname = data["name"]
        host.ipv4 = data["ipv4"]
        host.ipv6 = data["ipv6"]
    elif db == "port":
        port = Port.query.filter_by(id=data["id"]).first()
        port.port_number = data["port_number"]
    elif db == "tag":
        tag = Tag.query.filter_by(id=data["id"]).first()
        tag.tag_name = data["tag_name"]
    elif db == "host_tag":
        host_tag = HostTag.query.filter_by(id=data["id"]).first()
        host_tag.host_id = data["host_id"]
        host_tag.tag_id = data["tag_id"]
    elif db == "portFB":
        portFB = PortFB.query.filter_by(id=data["id"]).first()
        portFB.portFB_number = data["portFB_number"]
    else:
        print("Error: Database not found")
        




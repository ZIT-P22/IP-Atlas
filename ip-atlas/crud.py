# this Script contains the CRUD operations for the ip-atlas database
# Author: Janneck Lehmann
# Date: 2024-02-07
from models import Host, Port, Tag
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import atlasapp
from helper import *

DATABASE_URI = atlasapp.config["SQLALCHEMY_DATABASE_URI"]
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# function which converts the given data from db to the json format
def convert_to_json_format(hosts):
    data = {"hosts": []}
    for host in hosts:
        host_data = {
            "id": host.id,
            "name": host.hostname,
            "ip": host.ipv4,  
            "ports": [port.port_number for port in host.ports],
            "tags": [host_tag.tag.tag_name for host_tag in host.tags],
        }
        data["hosts"].append(host_data)
    return data

# function which reads all hosts from the database where the attribute deleted is set to false
def read_all_hosts():
    hosts = Host.query.filter_by(deleted=False).all()
    return hosts

# function which writes the given data to the database
def write_to_db(host_data):
    session = Session()
    hostname = host_data.get("name")
    ipv4 = host_data.get("ipv4")
    

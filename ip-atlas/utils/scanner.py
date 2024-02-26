import json
from utils.crud import *
from models import db, DiscoveredDevice
import os




# read the json file and return the data
def read_json(path = "ip-atlas/data/scanned_clients.json"):
    with open(path) as file:
        data = json.load(file)
    return data

# function which add the hosts to the database
def add_scanned_hosts():
    data = read_json()
    for host in data:
        discoveredDevice = DiscoveredDevice(mac_address=host["mac"], ipv4=host["ip"], vendor=host["vendor"])
        db.session.add(discoveredDevice)
    db.session.commit()
    
def scan_devices(range):
    # run the netscan.py script
    os.system("sudo python3 ip-atlas/utils/netscan.py -r " + range)
    add_scanned_hosts()
    print("Scanning complete")
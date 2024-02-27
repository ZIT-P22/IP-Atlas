import subprocess
import json
from utils.crud import *
from models import db, DiscoveredDevice
import os

password = os.getenv("PASSWORD")



# read the json file and return the data
def read_json(path = "ip-atlas/data/scanned_clients.json"):
    with open(path) as file:
        data = json.load(file)
    return data

# function which add the hosts to the database
def add_scanned_hosts():
    try:
        data = read_json()
        for host in data:
            discoveredDevice = DiscoveredDevice(mac_address=host["mac"], ipv4=host["ip"], vendor=host["vendor"])
            db.session.add(discoveredDevice)
        db.session.commit()
    except FileNotFoundError:
        print("JSON file not found. No hosts to add.")
    except json.decoder.JSONDecodeError:
        print("JSON decoding error. Check if the JSON file is valid.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def scan_devices(range):
    path_to_netscan = os.path.dirname(os.path.abspath(__file__)) + "/netscan.py"
    command = "sudo -S python3 "+  path_to_netscan + " -r " + range
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=f"{password}\n".encode())
    # print('Output:', stdout.decode())
    # print('Error:', stderr.decode())
    add_scanned_hosts()
    print("Scanning complete")

import subprocess
import json
from models import db, DiscoveredDevice
import os
from datetime import datetime

password = os.getenv("PASSWORD")



# read the json file and return the data
def read_json(path = "ip-atlas/data/scanned_clients.json"):
    # create file and folder if it does not exist
    if not os.path.exists("ip-atlas/data"):
        os.makedirs("ip-atlas/data")
        with open(path, "w") as file:
            file.write("[]")
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write("[]")
    with open(path) as file:
        data = json.load(file)
    return data

# function which add the hosts to the database
def add_scanned_hosts():
    try:
        data = read_json()
        for host in data:
            ipv4_address = host["ip"]
            existing_device = DiscoveredDevice.query.filter_by(ipv4=ipv4_address).first()
            if existing_device:
                existing_device.last_seen = datetime.utcnow()
                print("Diese IP gibt es bereits", ipv4_address)
            else:
                discoveredDevice = DiscoveredDevice(mac_address=host["mac"], ipv4=ipv4_address, vendor=host["vendor"])
                db.session.add(discoveredDevice)
        db.session.commit()
    except FileNotFoundError:
        print("JSON file not found. No hosts to add.")
    except json.decoder.JSONDecodeError:
        print("JSON decoding error. Check if the JSON file is valid.")
    except Exception as e:
        print(f"An error occurred: {e}")

    
def scan_devices(ip_range, adapter):
    path_to_netscan = os.path.dirname(os.path.abspath(__file__)) + "/netscan.py"
    command = f"sudo -S python3 {path_to_netscan} -r {ip_range} --iface {adapter}"
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=f"{password}\n".encode())
    print('Output:', stdout.decode())
    print('Error:', stderr.decode())
    add_scanned_hosts()
    print("Scanning complete")

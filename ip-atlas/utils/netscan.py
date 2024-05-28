import requests
from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup, BaseMacLookup
from time import time
import os
import json
from argparse import ArgumentParser

MAC_VENDOR_FILE = "ip-atlas/data/mac_vendors.txt"
SCANNED_CLIENTS_FILE = "ip-atlas/data/scanned_clients.json"
FLASK_SERVER_URL = "http://127.0.0.1:8080/add_devices"

def get_vendor(mac_address, mac_lookup_instance):
    try:
        vendor = mac_lookup_instance.lookup(mac_address)
        return vendor
    except Exception as e:
        print(f"Error looking up vendor for MAC {mac_address}: {e}")
        return "Unknown"

def wurde_vor_x_tagen_aktualisiert(dateipfad):
    try:
        letzte_aktualisierung = os.path.getmtime(dateipfad)
    except Exception as e:
        print(f"Error accessing file {dateipfad}: {e}")
        return False
    
    aktuelle_zeit = time()
    differenz_in_tagen = (aktuelle_zeit - letzte_aktualisierung) / (24 * 3600)
    return differenz_in_tagen >= 1

def update_vendor_list():
    init = False
    if not os.path.exists(MAC_VENDOR_FILE):
        try:
            with open(MAC_VENDOR_FILE, "w") as file:
                file.write("")
                init = True
        except Exception as e:
            print(f"Error creating file {MAC_VENDOR_FILE}: {e}")
            return None
            
    BaseMacLookup.cache_path = MAC_VENDOR_FILE
    mac_lookup_instance = MacLookup()
    
    if wurde_vor_x_tagen_aktualisiert(MAC_VENDOR_FILE) or init:
        try:
            mac_lookup_instance.update_vendors()
            print("Mac lookup updated")
        except Exception as e:
            print(f"Error updating Mac lookup: {e}")
    else:
        print("Mac lookup is up to date")
    
    return mac_lookup_instance

def update_vendor(clients):
    mac_lookup_instance = update_vendor_list()
    if mac_lookup_instance is None:
        print("Failed to initialize Mac lookup")
        return clients
    
    for client in clients:
        client['vendor'] = get_vendor(client['mac'], mac_lookup_instance)
        
    return clients

def get_devices(search_range, iface=None):
    arp = ARP(pdst=search_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    # Spezifische Netzwerkkarte verwenden
    result = srp(packet, iface=iface, timeout=3, verbose=0)[0]
    clients = [{'ip': received.psrc, 'mac': received.hwsrc, 'vendor': ''} for sent, received in result]
    
    clients = update_vendor(clients)
    print("Gefundene Geräte:", clients)
    save_as_json(clients)
    send_to_server(clients)
    return clients

def save_as_json(clients):
    try:
        if os.path.exists(SCANNED_CLIENTS_FILE):
            os.remove(SCANNED_CLIENTS_FILE)
            
        with open(SCANNED_CLIENTS_FILE, "w") as file:
            json.dump(clients, file, indent=4)
    except Exception as e:
        print(f"Error saving JSON file {SCANNED_CLIENTS_FILE}: {e}")

def send_to_server(clients):
    try:
        response = requests.post(FLASK_SERVER_URL, json={"devices": clients})
        if response.status_code == 201:
            print("Devices successfully sent to the server.")
        else:
            print(f"Failed to send devices. Server responded with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending devices to the server: {e}")

def args():
    parser = ArgumentParser(description="Python Script to Perform Network Scans")
    parser.add_argument("-r", "--range", dest="ip_range",
                        help="Specify an IP address range, e.g., --range 192.168.1.1/24")
    parser.add_argument("-i", "--iface", dest="iface",
                        help="Specify a network interface, e.g., --iface eth0")
    options = parser.parse_args()
    if not options.ip_range:
        parser.error("[-] Please specify a valid IP address range.")
    return options

def main():
    options = args()
    get_devices(options.ip_range, options.iface)
    print("Scan Finished")

if __name__ == "__main__":
    main()

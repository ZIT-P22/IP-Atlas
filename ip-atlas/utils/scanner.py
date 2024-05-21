from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup, BaseMacLookup
from time import time
import os
import json

MAC_VENDOR_FILE = "ip-atlas/data/mac_vendors.txt"
SCANNED_CLIENTS_FILE = "ip-atlas/data/scanned_clients.json"

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
    
    unique_macs = {client['mac'] for client in clients}
    mac_to_vendor = {}
    
    for mac in unique_macs:
        mac_to_vendor[mac] = get_vendor(mac, mac_lookup_instance)
    
    for client in clients:
        client['vendor'] = mac_to_vendor.get(client['mac'], "Unknown")
    
    return clients

def get_devices(search_range, iface=None):
    arp = ARP(pdst=search_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, iface=iface, timeout=3, verbose=0)[0]
    clients = [{'ip': received.psrc, 'mac': received.hwsrc, 'vendor': ''} for sent, received in result]
    
    clients = update_vendor(clients)
    print("Gefundene Geräte:", clients)
    save_as_json(clients)
    return clients

def save_as_json(clients):
    try:
        with open(SCANNED_CLIENTS_FILE, "w") as file:
            json.dump(clients, file, indent=4)
    except Exception as e:
        print(f"Error saving JSON file {SCANNED_CLIENTS_FILE}: {e}")

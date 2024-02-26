from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup, BaseMacLookup
from time import time
import os
import json
from argparse import ArgumentParser

# https://thepythoncode.com/article/building-network-scanner-using-scapy



def get_vendor(mac_address, mac ):
    try:
        vendor =  mac.lookup(mac_address)
        return vendor
    except:
        vendor = "Unknown"
        return vendor
    
def wurde_vor_x_tagen_aktualisiert(dateipfad):
    # Erhalte die Zeit der letzten Aktualisierung der Datei
    letzte_aktualisierung = os.path.getmtime(dateipfad)
    
    # Erhalte die aktuelle Zeit
    aktuelle_zeit = time()
    
    # Berechne die Differenz zwischen der aktuellen Zeit und der letzten Aktualisierung in Tagen
    differenz_in_tagen = (aktuelle_zeit - letzte_aktualisierung) / (24 * 3600)
    # print(differenz_in_tagen)
    # Überprüfe, ob die Differenz größer oder gleich 1 Tage ist
    if differenz_in_tagen >= 1:
        return True
    else:
        return False

def update_vendor_list():
    BaseMacLookup.cache_path = "ip-atlas/data/mac_vendors.txt"
    # wenn die datei das letzte mal vor mehr als 30 tagen geupdated wurde wird der update erneut ausgeführt
    mac = MacLookup()
    if wurde_vor_x_tagen_aktualisiert("ip-atlas/data/mac_vendors.txt"):
        mac.update_vendors()
        print("Mac lookup updated")
    else:
        print("Mac lookup is up to date")
    return mac

def update_vendor(clients):
    mac = update_vendor_list()
    for client in clients:
        client['vendor'] = get_vendor(client['mac'], mac)
    return clients

def get_devices(search_range):
    arp = ARP(pdst=search_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'vendor': ''})
    clients = update_vendor(clients)
    save_as_json(clients)
    return clients



# function which saves the clients to a json file
def save_as_json(clients):
    # delete old file
    if os.path.exists("ip-atlas/data/scanned_clients.json"):
        os.remove("ip-atlas/data/scanned_clients.json")
    with open("ip-atlas/data/scanned_clients.json", "w") as file:
        json.dump(clients, file, indent=4)



def args():
    parser = ArgumentParser(
        description="Python Script to Perform Network Scans")
    parser.add_argument("-r", "--range", dest="ip_range",
                        help="Specify an IP address range, e.g., --range 192.168.1.1/24")
    options = parser.parse_args()
    if not options.ip_range:
        parser.error("[-] Please specify a valid IP address range.")
    return options

def main():
    options = args()
    get_devices(options.ip_range)




























if __name__ == "__main__":
    # print(get_devices("192.168.211.226/24"))
    main()





#target_ip = "192.69.69.1/24"
# target_ip = "192.168.42.0/24"

# IP Address for the destination
# create ARP packet
# arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
# ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
# packet = ether/arp

# result = srp(packet, timeout=3, verbose=0)[0]

# a list of clients, we will fill this in the upcoming loop
# clients = []

# for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    # clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
# print("Available devices in the network:")
# print("IP" + " "*18+"MAC" + " "*18 + "Vendor")
# for client in clients:
#     print("{:16}    {}".format(client['ip'], client['mac']), end="    ")
#     try:
#         print(mac.lookup(client['mac']))
#     except:
#         print("Unknown")

#print(clients)
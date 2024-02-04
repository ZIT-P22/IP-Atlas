import sys
import datetime as dt
import requests
from prettytable import PrettyTable, HEADER, NONE
from argparse import ArgumentParser
import scapy.all as scapy
from pythonping import ping
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import time
import json
from functools import lru_cache

# Function Definitions


def args():
    parser = ArgumentParser(
        description="Python Script to Perform Network Scans")
    parser.add_argument("-r", "--range", dest="ip_range",
                        help="Specify an IP address range, e.g., --range 192.168.1.1/24")
    parser.add_argument("-s", "--scan", dest="scan_type",
                        help="Scan type: arp, icmp, sniff, meta", default="meta")
    options = parser.parse_args()
    if not options.ip_range:
        parser.error("[-] Please specify a valid IP address range.")
    return options


def icmp_ping_scan(ip_range):
    print("[*] Starting ICMP Ping Scan")
    live_hosts = []
    network = ipaddress.ip_network(ip_range, strict=False)
    for ip in network.hosts():
        response = ping(str(ip), count=1, timeout=1)
        if response.success():
            live_hosts.append(str(ip))
    return live_hosts


def icmp_ping_individual(ip):
    response = ping(ip, count=1, timeout=1)
    if response.success():
        return (ip, "Unknown MAC", 'ICMP')
    return None


def arp_ping_scan(ip_range):
    print("[*] Starting ARP Ping Scan")
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return [(received.psrc, received.hwsrc, 'ARP') for sent, received in answered]


def sniff_packets(timeout=5):
    print("[*] Starting Sniffing in Promiscuous Mode")
    packets = scapy.sniff(timeout=timeout)
    return [(packet[scapy.IP].src, packet[scapy.Ether].src, 'Sniff') for packet in packets if scapy.IP in packet and scapy.Ether in packet]


@lru_cache(maxsize=None)
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return 'Unknown'


@lru_cache(maxsize=None)
def vendor_lookup(mac):
    time.sleep(1)
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImp0aSI6IjMzMTZjODI4LWEwODAtNDQ4NS1hMmEwLWE2ZTNkNmJmZjY2MCJ9.eyJpc3MiOiJtYWN2ZW5kb3JzIiwiYXVkIjoibWFjdmVuZG9ycyIsImp0aSI6IjMzMTZjODI4LWEwODAtNDQ4NS1hMmEwLWE2ZTNkNmJmZjY2MCIsImlhdCI6MTcwNjk5ODMwMiwiZXhwIjoyMDIxNDk0MzAyLCJzdWIiOiIxNDE4MyIsInR5cCI6ImFjY2VzcyJ9.8IbatiRNBLYLh5m4S28RCnAOQ1YRhJcC7Ha_RFiDEwjyJ7a2Ts1HUC7Pp9eN_warWBAD9Ch89-KAwyIo0aGVEA"}
    try:
        response = requests.get(
            f"https://api.macvendors.com/v1/lookup/{mac}", headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()["data"]["organization_name"]
    except Exception as e:
        print(f"Error fetching vendor for MAC {mac}: {e}")
    return "Unknown"


def run_scan(option):
    results = []
    max_threads = 50
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        if option.scan_type in ["arp", "icmp", "meta"]:
            network = ipaddress.ip_network(option.ip_range, strict=False)
            if option.scan_type == "arp":
                futures.append(executor.submit(arp_ping_scan, option.ip_range))
            elif option.scan_type == "icmp":
                for ip in network.hosts():
                    futures.append(executor.submit(
                        icmp_ping_individual, str(ip)))
            elif option.scan_type == "meta":
                futures.append(executor.submit(arp_ping_scan, option.ip_range))
                for ip in network.hosts():
                    futures.append(executor.submit(
                        icmp_ping_individual, str(ip)))
                futures.append(executor.submit(sniff_packets))
        elif option.scan_type == "sniff":
            futures.append(executor.submit(sniff_packets))

        for future in as_completed(futures):
            result = future.result()
            if result:
                if isinstance(result, list):
                    results.extend(result)
                else:
                    results.append(result)

    return results


def main():
    option = args()
    print("\n---------------------")
    print("Start time: " + dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p"))
    print("Target subnet: " + option.ip_range)
    print("Scan type: " + option.scan_type)
    print("---------------------\n")

    all_results = run_scan(option)
    subnet = ipaddress.ip_network(option.ip_range, strict=False)

    merged_results = {}

    for ip, mac, scan_type in all_results:
        if ipaddress.ip_address(ip) in subnet:
            if ip not in merged_results:
                merged_results[ip] = {'macs': set(), 'scan_types': set(), 'vendors': [
                ], 'hostname': 'Unknown'}

            entry = merged_results[ip]
            entry['scan_types'].add(scan_type)

            if mac != "Unknown MAC":
                entry['macs'].add(mac)

            current_hostname = get_hostname(ip)
            if current_hostname != 'Unknown' and (entry['hostname'] == 'Unknown' or len(current_hostname) > len(entry['hostname'])):
                entry['hostname'] = current_hostname

    for ip, details in merged_results.items():
        for mac in details['macs']:
            vendor = vendor_lookup(mac)
            if vendor != "Unknown":
                details['vendors'].append(vendor)

    for ip, details in merged_results.items():
        details['macs'] = list(details['macs'])
        details['scan_types'] = list(details['scan_types'])

    results_json = json.dumps(merged_results, indent=4)
    print(results_json)
    print("---------------------\nFinished!")


if __name__ == "__main__":
    main()

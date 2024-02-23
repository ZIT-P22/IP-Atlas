import sys
import datetime as dt
import requests
import scapy.all as scapy
from pythonping import ping
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import json
from functools import lru_cache
import time
from argparse import ArgumentParser
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


def chunk_ip_range(ip_range, chunk_size=256):
    """Generate sub-ranges from a larger IP range."""
    network = ipaddress.ip_network(ip_range, strict=False)
    for i in range(0, int(network.num_addresses), chunk_size):
        start_ip = network.network_address + i
        end_ip = min(start_ip + chunk_size - 1, network.broadcast_address)
        yield ipaddress.ip_network(f"{start_ip}/{start_ip.max_prefixlen}", strict=False).supernet(new_prefix=network.prefixlen)


def icmp_ping_individual(ip):
    response = ping(ip, count=1, timeout=1)
    if response.success():
        return (ip, "Unknown MAC", 'ICMP')
    return None


def arp_ping_scan(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return [(received.psrc, received.hwsrc, 'ARP') for sent, received in answered]


def sniff_packets(timeout=5):
    packets = scapy.sniff(timeout=timeout)
    return [(packet[scapy.IP].src, packet[scapy.Ether].src, 'Sniff') for packet in packets if scapy.IP in packet and scapy.Ether in packet]


@lru_cache(maxsize=1024)
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return 'Unknown'


@lru_cache(maxsize=1024)
def vendor_lookup(mac):
    # Mock delay for demonstration; adjust according to your rate limiting
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
            # Implement IP Range Chunking for ARP and ICMP scans
            if option.scan_type in ["arp", "meta"]:
                for chunk in chunk_ip_range(option.ip_range):
                    futures.append(executor.submit(arp_ping_scan, str(chunk)))
            if option.scan_type in ["icmp", "meta"]:
                for chunk in chunk_ip_range(option.ip_range):
                    chunk_network = ipaddress.ip_network(chunk, strict=False)
                    for ip in chunk_network.hosts():
                        futures.append(executor.submit(
                            icmp_ping_individual, str(ip)))
            if option.scan_type in ["sniff", "meta"]:
                futures.append(executor.submit(sniff_packets))

        # Process futures as they complete
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
    merged_results = {}
    for ip, mac, scan_type in all_results:
        if ip not in merged_results:
            merged_results[ip] = {'macs': set(), 'scan_types': set(), 'vendors': [
            ], 'hostname': 'Unknown'}
        merged_results[ip]['scan_types'].add(scan_type)
        if mac != "Unknown MAC":
            merged_results[ip]['macs'].add(mac)
            vendor = vendor_lookup(mac)
            if vendor not in merged_results[ip]['vendors']:
                merged_results[ip]['vendors'].append(vendor)
        if merged_results[ip]['hostname'] == 'Unknown':
            hostname = get_hostname(ip)
            if hostname != 'Unknown':
                merged_results[ip]['hostname'] = hostname

    # Convert sets to lists for JSON serialization
    for ip in merged_results:
        merged_results[ip]['macs'] = list(merged_results[ip]['macs'])
        merged_results[ip]['scan_types'] = list(
            merged_results[ip]['scan_types'])

    print(json.dumps(merged_results, indent=4))


print("---------------------\nFinished!")

if __name__ == "__main__":
    main()
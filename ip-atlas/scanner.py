import datetime as dt
import requests
import scapy.all as scapy
from pythonping import ping
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import socket
import time
import json
from functools import lru_cache
import numpy as np
from ipaddress import IPv4Address


def chunk_subnets(network, chunk_size=24):
    return list(network.subnets(new_prefix=chunk_size))


def filter_subnets(all_subnets, selected_subnets):
    selected_networks = [ipaddress.ip_network(subnet) for subnet in selected_subnets]
    return [
        subnet
        for subnet in all_subnets
        if any(subnet.overlaps(selected) for selected in selected_networks)
    ]


def icmp_ping_scan(ip, fast=True):
    response = ping(str(ip), count=1, timeout=1 if fast else 2)
    if response.success():
        return str(ip)
    return None


def arp_ping_scan(ip):
    arp_request = scapy.ARP(pdst=str(ip))
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return [(received.psrc, received.hwsrc) for _, received in answered]


@lru_cache(maxsize=None)
def get_hostname(ip):
    # Ensure ip is a string before passing it to gethostbyaddr
    if isinstance(ip, IPv4Address):
        ip = str(ip)
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        # Handle the case where the host name could not be resolved
        return None


@lru_cache(maxsize=None)
def vendor_lookup(mac):
    time.sleep(1)
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImp0aSI6IjMzMTZjODI4LWEwODAtNDQ4NS1hMmEwLWE2ZTNkNmJmZjY2MCJ9.eyJpc3MiOiJtYWN2ZW5kb3JzIiwiYXVkIjoibWFjdmVuZG9ycyIsImp0aSI6IjMzMTZjODI4LWEwODAtNDQ4NS1hMmEwLWE2ZTNkNmJmZjY2MCIsImlhdCI6MTcwNjk5ODMwMiwiZXhwIjoyMDIxNDk0MzAyLCJzdWIiOiIxNDE4MyIsInR5cCI6ImFjY2VzcyJ9.8IbatiRNBLYLh5m4S28RCnAOQ1YRhJcC7Ha_RFiDEwjyJ7a2Ts1HUC7Pp9eN_warWBAD9Ch89-KAwyIo0aGVEA"
    }
    try:
        response = requests.get(
            f"https://api.macvendors.com/v1/lookup/{mac}", headers=headers, timeout=5
        )
        if response.status_code == 200:
            return response.json()["data"]["organization_name"]
    except Exception as e:
        print(f"Error fetching vendor for MAC {mac}: {e}")
    return "Unknown"


def process_device(ip, fast_scan=True):
    # Convert IPv4Address to string if necessary
    ip_str = str(ip) if isinstance(ip, IPv4Address) else ip
    device_info = {"ip": ip_str, "hostname": get_hostname(ip_str), "macs": []}
    if not fast_scan:
        arp_results = arp_ping_scan(ip_str)
        for psrc, hwsrc in arp_results:
            device_info["macs"].append({"mac": hwsrc, "vendor": vendor_lookup(hwsrc)})
    return device_info


def initialize_results_file(filename="scan_results.json"):
    try:
        with open(filename, "r") as file:
            # Check if file is empty or contains valid JSON
            try:
                data = json.load(file)
                if not isinstance(data, list):  # Ensure data is a list
                    raise ValueError("File content is not a list")
            except json.JSONDecodeError:
                # File is empty or not valid JSON, start with an empty list
                with open(filename, "w") as file:
                    json.dump([], file, indent=4)
    except FileNotFoundError:
        # File does not exist, create it with an empty list
        with open(filename, "w") as file:
            json.dump([], file, indent=4)


def save_results_to_file(results, filename="scan_results.json"):
    with open(filename, "w") as file:
        json.dump(results, file, indent=4)


def run_scan(scan_type, ip_range, selected_subnets):
    network = ipaddress.ip_network(ip_range, strict=False)
    all_subnets = chunk_subnets(network)
    subnets_to_scan = (
        filter_subnets(all_subnets, selected_subnets)
        if selected_subnets
        else all_subnets
    )

    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for subnet in subnets_to_scan:
            for ip in subnet.hosts():
                if scan_type == "fast":
                    future = executor.submit(icmp_ping_scan, ip, True)
                else:
                    future = executor.submit(icmp_ping_scan, ip, False)
                future.add_done_callback(
                    lambda fut, ip=ip: (
                        results.append(process_device(ip, scan_type == "fast"))
                        if fut.result()
                        else None
                    )
                )

    # Wait for all futures to complete
    as_completed(futures)

    # Save results to file
    save_results_to_file(results)


# @app.route("/scan", methods=["POST"])
# def scan_network():
#     data = request.get_json()
#     scan_type = data.get("scan_type", "fast")
#     ip_range = data.get("ip_range")
#     selected_subnets = data.get("selected_subnets", [])

#     if not ip_range:
#         return jsonify({"error": "IP range is required"}), 400

#     run_scan(scan_type, ip_range, selected_subnets)
#     return jsonify({"message": "Scan initiated"}), 202


# if __name__ == "__main__":
#     app.run(debug=True)

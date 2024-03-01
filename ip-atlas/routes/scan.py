from utils.scanner import scan_devices
from flask import Blueprint, jsonify, render_template

scan = Blueprint("scan", __name__)


@scan.route("/discovered")
def discovered():
    # Instead of loading data from a JSON file, we'll create a sample data dictionary directly in the code.
    # This sample data mimics the structure that would be expected by the 'ip/discovered.html' template.
    
    scan_devices("192.168.107.226/24")
    # data = {
    #     "name": "Sample Device",
    #     "ip": "192.168.1.1",
    #     "hostname": "sample-device.local",
    #     "mac": "00:1B:44:11:3A:B7",
    #     "os": "Linux",
    #     "last_active": "2023-04-01 12:34:56",
    # }
    devices = convert_discovered_devices_to_json_format()
    print(devices)
    return render_template("ip/discovered.html", devices=devices)


# @scan.route("/scan/fast")
# def scan_fast():
#     # Define the IP range for the scan
#     ip_range = "192.168.178.0/24"
#     # No specific subnets selected for this example
#     selected_subnets = []
#     # Initiate a fast scan
#     try:
#         run_scan("fast", ip_range, selected_subnets)
#         return jsonify({"message": "Fast scan initiated successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @scan.route("/scan/advanced")
# def scan_advanced():
#     # Define the IP range for the scan
#     ip_range = "192.168.178.0/24"
#     # No specific subnets selected for this example
#     selected_subnets = []
#     # Initiate an advanced (deep) scan
#     try:
#         run_scan("deep", ip_range, selected_subnets)
#         return jsonify({"message": "Advanced scan initiated successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

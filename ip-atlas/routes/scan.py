from utils.scanner import scan_devices
from flask import Blueprint, jsonify, render_template
from utils.crud import convert_discovered_devices_to_json_format

scan = Blueprint("scan", __name__)


@scan.route("/discovered")
def discovered():
    scan_devices("192.69.69.1/24")
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

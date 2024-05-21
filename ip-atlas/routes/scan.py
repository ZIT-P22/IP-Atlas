from concurrent.futures import ThreadPoolExecutor
from utils.scanner import scan_devices
from flask import Blueprint, jsonify, render_template, request
from utils.crud import convert_discovered_devices_to_json_format, get_tags, set_used_of_discovered_device, write_edit_db
from utils.settings import load_settings
from models import Host, db, DiscoveredDevice
import time

scan = Blueprint("scan", __name__)

@scan.route("/discovered")
def discovered():
    settings = load_settings()
    ip_ranges = settings.get("ip_ranges", [])

    start_time = time.time()

    # Parallelisierung der Scanvorgänge
    def scan_wrapper(ip_range):
        scan_devices(ip_range["range"], ip_range["interface"])

    with ThreadPoolExecutor() as executor:
        executor.map(scan_wrapper, ip_ranges)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Scan duration: {duration} seconds")

    # Gefundene Geräte und Tags abrufen
    devices = convert_discovered_devices_to_json_format()
    tags = get_tags()
    return render_template("ip/discovered.html", devices=devices, tags=tags)

@scan.route("/set_used/<int:id>", methods=["POST"])
def set_used(id):
    status = set_used_of_discovered_device(id)
    return jsonify({"status": status})

@scan.route("/check_ipv4/<ipv4>", methods=["GET"])
def check_ipv4(ipv4):
    device = Host.query.filter_by(ipv4=ipv4).first()
    if device:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})

@scan.route("/edit_device", methods=["POST"])
def edit_device():
    formData = request.form
    success = write_edit_db(formData)
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})
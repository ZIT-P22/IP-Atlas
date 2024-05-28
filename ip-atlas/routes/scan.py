from flask import Blueprint, jsonify, render_template, request
from utils.scanner import start_background_scan, get_scan_progress
from utils.crud import convert_discovered_devices_to_json_format, get_tags, set_used_of_discovered_device, write_edit_db
from utils.settings import load_settings
from models import Host, DiscoveredDevice, db
from datetime import datetime

scan = Blueprint("scan", __name__)

@scan.route("/discovered")
def discovered():
    # Gefundene Geräte und Tags abrufen
    devices = convert_discovered_devices_to_json_format()
    tags = get_tags()
    print(devices)  # Debug-Ausgabe
    print(tags)     # Debug-Ausgabe
    return render_template("ip/discovered.html", devices=devices, tags=tags)

@scan.route("/start_scan", methods=["POST"])
def start_scan():
    settings = load_settings()
    ip_ranges = settings.get("ip_ranges", [])
    
    start_background_scan(ip_ranges)
    
    return jsonify({"status": "scan_started"})

@scan.route("/scan_progress", methods=["GET"])
def scan_progress():
    progress = get_scan_progress()
    return jsonify(progress)

@scan.route("/get_results", methods=["GET"])
def get_results():
    devices = convert_discovered_devices_to_json_format()
    return jsonify({"devices": devices})

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
    
@scan.route("/add_devices", methods=["POST"])
def add_devices():
    devices = request.json.get("devices", [])
    for client in devices:
        ipv4_address = client["ip"]
        existing_device = DiscoveredDevice.query.filter_by(ipv4=ipv4_address).first()
        if existing_device:
            existing_device.last_seen = datetime.utcnow()
            print("Diese IP gibt es bereits", ipv4_address)
        else:
            discovered_device = DiscoveredDevice(
                mac_address=client["mac"],
                ipv4=ipv4_address,
                vendor=client["vendor"],
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow()
            )
            db.session.add(discovered_device)
    db.session.commit()
    return jsonify({"status": "devices_added"}), 201

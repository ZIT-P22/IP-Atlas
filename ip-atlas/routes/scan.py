from utils.scanner import scan_devices
from flask import Blueprint, jsonify, render_template, request
from utils.crud import convert_discovered_devices_to_json_format, get_tags, set_used_of_discovered_device, write_edit_db
from models import Host

scan = Blueprint("scan", __name__)

@scan.route("/discovered")
def discovered():
    # scan_devices("172.23.87.15/20","eth0")
    # scan_devices("172.10.2.129/20","wlo1")
    devices = convert_discovered_devices_to_json_format()
    tags = get_tags()
    print(devices)
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

from utils.scanner import scan_devices
from flask import Blueprint, jsonify, render_template
from utils.crud import convert_discovered_devices_to_json_format, get_tags, set_used_of_discovered_device

scan = Blueprint("scan", __name__)

@scan.route("/discovered")
def discovered():
    scan_devices("192.168.42.162/24","wlo1")
    devices = convert_discovered_devices_to_json_format()
    tags = get_tags()
    print(devices)
    return render_template("ip/discovered.html", devices=devices, tags=tags)


@scan.route("/set_used/<int:id>", methods=["POST"])
def set_used(id):
    status = set_used_of_discovered_device(id)
    return jsonify({"status": status})


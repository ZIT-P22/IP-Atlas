from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from utils.filter import filterAll, filter_data, isIpPingable
from utils.crud import (
    write_host_to_db,
    write_edit_db,
    delete_host_by_id,
    revert_host_by_id,
    permanently_delete_host_by_id,  # Neue Funktion für endgültiges Löschen
    return_json_format,
    check_ipv4_exists,
    get_tags,
)
from colorama import Fore, Style

atlas = Blueprint("atlas", __name__)

@atlas.route("/")
def index():
    data = return_json_format()
    return render_template("dashboard.html", data=data)

@atlas.route("/ip/list")
def list():
    data = return_json_format()
    return render_template("ip/list.html", data=data)

@atlas.route("/ip/ping/<ip_address>")
def ping_ip(ip_address):
    pingable = isIpPingable(ip_address)
    return jsonify({"pingable": pingable})

@atlas.route("/ip/add")
def add():
    tags = get_tags()
    return render_template("ip/add.html", tags=tags)

@atlas.route("/ip/save", methods=["POST"])
def save():
    if request.method == "POST":
        formData = request.form
        if not check_ipv4_exists(formData.get("ipv4")):
            write_host_to_db(formData)
            return redirect(url_for("atlas.list"))
        else:
            return "IP address already exists"

@atlas.route("/ip/update/<int:id>", methods=["POST"])
def update_ip(id):
    if request.method == "POST":
        data = request.json
        data["id"] = id
        success = write_edit_db(data)
        if success:
            return jsonify({"message": "IP address updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update IP address"}), 500

# Route für das Verschieben in den Papierkorb
@atlas.route("/ip/delete/<int:id>")
def delete(id):
    confirmed = request.args.get("confirmed")
    if confirmed == "true":
        if delete_host_by_id(id):
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Deletion failed")
    else:
        return jsonify(success=False, message="Deletion not confirmed")

@atlas.route("/port/list")
def port():
    return render_template("port/list.html")

@atlas.route("/statistic")
def statistic():
    return render_template("statistic.html")

@atlas.route("/search", methods=["GET"])
def search():
    search_query = request.args.get("q", default="", type=str)
    search_type = request.args.get("search_type", default="ip", type=str)
    data = return_json_format()
    if search_type in ["ip", "name", "port", "tag"]:
        filtered_data = filter_data(search_query, search_type, data)
    else:
        filtered_data = data["hosts"]
    return render_template("ip/list.html", data={"hosts": filtered_data})

@atlas.route("/filter", methods=["GET"])
def filter():
    data = return_json_format()
    name = request.args.get("name", "")
    ipocted1 = request.args.get("ipocted1", "")
    ipocted2 = request.args.get("ipocted2", "")
    ipocted3 = request.args.get("ipocted3", "")
    ipocted4 = request.args.get("ipocted4", "")
    tags = request.args.get("tags", "")
    ports = request.args.get("ports", "")
    ip = f"{ipocted1}.{ipocted2}.{ipocted3}.{ipocted4}"
    filtered_data = filterAll(ip, name, ports, tags, data)
    return render_template("ip/list.html", data=filtered_data)

@atlas.route("/ip/trashcan/list")
def list_trashcan():
    data = return_json_format("deleted")
    return render_template("ip/trashcan/list.html", data=data)

# Neue Route für das endgültige Löschen
@atlas.route("/ip/delete/permanent/<int:id>")
def delete_permanent(id):
    confirmed = request.args.get("confirmed")
    if confirmed == "true":
        if permanently_delete_host_by_id(id):
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Permanent deletion failed")
    else:
        return jsonify(success=False, message="Permanent deletion not confirmed")

@atlas.route("/filter/trashcan", methods=["GET"])
def filter_trashcan():
    data = return_json_format("deleted")
    name = request.args.get("name", "")
    ipocted1 = request.args.get("ipocted1", "")
    ipocted2 = request.args.get("ipocted2", "")
    ipocted3 = request.args.get("ipocted3", "")
    ipocted4 = request.args.get("ipocted4", "")
    tags = request.args.get("tags", "")
    ports = request.args.get("ports", "")
    ip = f"{ipocted1}.{ipocted2}.{ipocted3}.{ipocted4}"
    filtered_data = filterAll(ip, name, ports, tags, data)
    return render_template("ip/trashcan/list.html", data=filtered_data)


@atlas.route("/ip/delete/revert/<int:id>")
def revert_trashcan(id):
    confirmed = request.args.get("confirmed")
    print(f"Reverting host with id {id}, confirmed={confirmed}")  # Debugging-Ausgabe
    if confirmed == "true":
        success = revert_host_by_id(id)
        if success:
            print(f"Successfully reverted host with id {id}")  # Debugging-Ausgabe
            return jsonify(success=True)
        else:
            print(f"Failed to revert host with id {id}")  # Debugging-Ausgabe
            return jsonify(success=False, message="Revert failed")
    else:
        print("Revert not confirmed")  # Debugging-Ausgabe
        return jsonify(success=False, message="Revert not confirmed")

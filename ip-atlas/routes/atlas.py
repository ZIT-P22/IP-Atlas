from flask import Blueprint, render_template, request, abort, jsonify
from jinja2 import TemplateNotFound
from helper import *
from filter import *

bp_atlas = Blueprint("atlas", __name__)


@bp_atlas.route("/")
def index():
    createJson()
    data = loadJson()
    return render_template("dashboard.html", data=data)


@bp_atlas.route("/ip/list")
def list():
    createJson()
    data = loadJson()
    return render_template("ip/list.html", data=data)


@bp_atlas.route("/ip/ping/<ip_address>")
def ping_ip(ip_address):
    pingable = isIpPingable("127.0.0.1")
    # pingable = isIpPingable(ip_address)
    return jsonify({"pingable": pingable})


@bp_atlas.route("/ip/<id>")
def show(id):
    createJson()
    # get type of id
    id = int(id)
    # print("ID:",id,":")
    data = getHostById(id)
    # print("Daten der ID: ", id, " :", data)
    return render_template("ip/show.html", data=data)


# add new host


@bp_atlas.route("/ip/add")
def add():
    return render_template("ip/add.html")


@bp_atlas.route("/ip/save", methods=["POST"])
def save():
    if request.method == "POST":
        # get form data
        name = request.form.get("name")
        tags = request.form.get("tags")
        ipv4 = request.form.get("ipv4")
        ipv6 = request.form.get("ipv6")
        ports = request.form.get("ports")
        tags = request.form.get("tags")

        if ports:
            # convert ports from comma separated to list
            ports = ports.split(",")
        if tags:
            # convert tags from comma separated to list
            tags = tags.split(",")

        # print(name, ipv4, ipv6, ports)
        writeJson(name, ipv4, tags, ipv6, ports)
        data = loadJson()
    return render_template("ip/list.html", data=data)


@bp_atlas.route("/ip/update/<int:id>", methods=["POST"])
def update_ip(id):
    if request.method == "POST":
        data = request.json
        # Assuming you have a function to update the IP address by ID
        success = updateIpAddressById(id, data)
        if success:
            return jsonify({"message": "IP address updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update IP address"}), 500


# delete host
@bp_atlas.route("/ip/delete/<id>")
def delete(id):
    id = int(id)
    confirmed = request.args.get("confirmed")
    data = loadJson()

    if confirmed == "true":
        deleteHost(id)
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Deletion not confirmed")


# confirm delete host


@bp_atlas.route("/ip/confirmdel/<id>")
def confirmdel(id):
    id = int(id)
    data = getHostById(id)
    return render_template("ip/confirmdel.html", data=data)


@bp_atlas.route("/port/list")
def port():

    return render_template("port/list.html")


@bp_atlas.route("/statistic")
def statistic():
    return render_template("statistic.html")


@bp_atlas.route("/search", methods=["GET"])
def search():
    # Retrieve search parameters from the request
    search_query = request.args.get("q", default="", type=str)
    search_type = request.args.get("search_type", default="ip", type=str)

    # Load the JSON data
    data = loadJson()

    # Filter the data based on the search parameters
    if search_type in ["ip", "name", "port", "tag"]:
        filtered_data = filter_data(search_query, search_type, data)
    else:
        # If the search type is not recognized, return the unfiltered data
        filtered_data = data["hosts"]

    # Render the template with the filtered data
    return render_template("ip/list.html", data={"hosts": filtered_data})


@bp_atlas.route("/filter", methods=["GET"])
def filter():
    data = loadJson()
    # Retrieve query parameters
    name = request.args.get("name", "")
    ipocted1 = request.args.get("ipocted1", "")
    ipocted2 = request.args.get("ipocted2", "")
    ipocted3 = request.args.get("ipocted3", "")
    ipocted4 = request.args.get("ipocted4", "")
    tags = request.args.get("tags", "")
    ports = request.args.get("ports", "")
    print("Filter: ", name, ipocted1, ipocted2, ipocted3, ipocted4, tags, ports)
    # Combine IP octets into a single string
    ip = f"{ipocted1}.{ipocted2}.{ipocted3}.{ipocted4}"
    print("IP: ", ip)

    # Call the filterAll function with the collected parameters
    filtered_data = filterAll(ip, name, ports, tags, data)
    print("Filtered data: ", filtered_data)

    # Render the template with the filtered data
    return render_template("ip/list.html", data=filtered_data)


#! Trashcan
@bp_atlas.route("/ip/trashcan/list")
def listTrashcan():
    createJson()
    data = loadTrashJson()
    return render_template("ip/trashcan/list.html", data=data)


@bp_atlas.route("/ip/delete/revert/<id>")
def revertTrashcan(id):
    id = int(id)
    confirmed = request.args.get("confirmed")
    data = loadTrashJson()

    if confirmed == "true":
        deleteTrashHost(id)
        # print("Host with id: ", id, " deleted")
        return render_template("ip/trashcan/list.html", data=data)
    else:
        return render_template("ip/trashcan/list.html", data=data)


@bp_atlas.route("/filter/trashcan", methods=["GET"])
def filterTrashcan():
    data = loadTrashJson()
    # Retrieve query parameters
    name = request.args.get("name", "")
    ipocted1 = request.args.get("ipocted1", "")
    ipocted2 = request.args.get("ipocted2", "")
    ipocted3 = request.args.get("ipocted3", "")
    ipocted4 = request.args.get("ipocted4", "")
    tags = request.args.get("tags", "")
    ports = request.args.get("ports", "")
    print("Filter: ", name, ipocted1, ipocted2, ipocted3, ipocted4, tags, ports)
    # Combine IP octets into a single string
    ip = f"{ipocted1}.{ipocted2}.{ipocted3}.{ipocted4}"
    print("IP: ", ip)

    # Call the filterAll function with the collected parameters
    filtered_data = filterAll(ip, name, ports, tags, data)
    print("Filtered data: ", filtered_data)

    # Render the template with the filtered data
    return render_template("ip/trashcan/list.html", data=filtered_data)

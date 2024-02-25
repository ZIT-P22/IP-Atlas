from flask import Blueprint, render_template, request, abort, jsonify
from utils.filter import *
from utils.crud import *
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
    pingable = isIpPingable("127.0.0.1")
    # pingable = isIpPingable(ip_address)
    return jsonify({"pingable": pingable})





# add new host
@atlas.route("/ip/add")
def add():
    return render_template("ip/add.html")


@atlas.route("/ip/save", methods=["POST"])
def save():
    if request.method == "POST":
        # get form data
        formData = request.form
        if not check_ipv4_exists(formData.get("ipv4")):
            write_host_to_db(formData)
            data = return_json_format()
            return render_template("ip/list.html", data=data)
        else:
            return "IP address already exists"


@atlas.route("/ip/update/<int:id>", methods=["POST"])
def update_ip(id):
    print(Fore.RED + "Update IP" + Style.RESET_ALL)
    if request.method == "POST":
        data = request.json
        data["id"] = id
        # print(data)
        
        success = write_edit_db(data)
         
        if success:
            return jsonify({"message": "IP address updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update IP address"}), 500


# delete host
@atlas.route("/ip/delete/<id>")
def delete(id):
    id = int(id)
    confirmed = request.args.get("confirmed")
    if confirmed == "true":
        delete_host_by_id(id)    
        return jsonify(success=True)
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
    # Retrieve search parameters from the request
    search_query = request.args.get("q", default="", type=str)
    search_type = request.args.get("search_type", default="ip", type=str)

    # Load the JSON data
    data = return_json_format()

    # Filter the data based on the search parameters
    if search_type in ["ip", "name", "port", "tag"]:
        filtered_data = filter_data(search_query, search_type, data)
    else:
        # If the search type is not recognized, return the unfiltered data
        filtered_data = data["hosts"]

    # Render the template with the filtered data
    return render_template("ip/list.html", data={"hosts": filtered_data})


@atlas.route("/filter", methods=["GET"])
def filter():
    data = return_json_format()
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
@atlas.route("/ip/trashcan/list")
def listTrashcan():
    data = return_json_format("deleted")
    return render_template("ip/trashcan/list.html", data=data)


@atlas.route("/ip/delete/revert/<id>")
def revertTrashcan(id):
    id = int(id)
    confirmed = request.args.get("confirmed")
    
    if confirmed == "true":
        revert_host_by_id(id)
        data = return_json_format()
        return render_template("ip/trashcan/list.html", data=data)
    else:
        data = return_json_format()
        return render_template("ip/trashcan/list.html", data=data)


@atlas.route("/filter/trashcan", methods=["GET"])
def filterTrashcan():
    data = return_json_format("deleted")
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

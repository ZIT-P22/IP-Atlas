
# this Script contains the CRUD operations for the ip-atlas table
# Author: Janneck Lehmann
# Date: 2024-02-07
from models import db, Host, Tag, Port, HostTag, PortFB
from helper import *




# function which converts the given data from db to the json format
def convert_to_json_format(host):
    host_data = {
        "id": host.id,
        "name": host.hostname,
        "ip": host.ipv4,
        "ipv6": host.ipv6,  
        "portsFB": [portFB.portFB_number for portFB in host.portsFB],
        "tags": [host_tag.tag.tag_name for host_tag in host.tags],
    }
    return host_data

# creates the json format after the data is loaded from the table
def return_json_format():
    data = {"hosts": []}
    hosts = read_all_hosts()
    for host in hosts:
        data["hosts"].append(convert_to_json_format(host))
    return data

# function which reads the host from the table by the given id
def get_host_by_id(id):
    host = Host.query.filter_by(id=id).first()
    return convert_to_json_format(host)

#

# function which reads all hosts from the table where the attribute deleted is set to false
def read_all_hosts():
    hosts = Host.query.filter_by(deleted=False).all()
    return hosts

# function which writes the given data to the table
def write_to_db(table, data):
    if table == "host":
        host = Host(hostname=data["name"], ipv4=data["ipv4"], ipv6=data["ipv6"])
        db.session.add(host)
    elif table == "port":
        port = Port(host_id=data["host_id"], port_number=data["port_number"])
        db.session.add(port)
    elif table == "tag":
        tag = Tag(tag_name=data["tag_name"])
        db.session.add(tag)
    elif table == "host_tag":
        host_tag = HostTag(host_id=data["host_id"], tag_id=data["tag_id"])
        db.session.add(host_tag)
    elif table == "portFB":
        portFB = PortFB(host_id=data["host_id"], portFB_number=data["portFB_number"])
        db.session.add(portFB)
    else:
        print("Error: table not found")

# function which writes an host to the db
def write_host_to_db(formData):
    name = formData.get("name")
    tags = formData.get("tags")
    ipv4 = formData.get("ipv4")
    ipv6 = formData.get("ipv6")
    portsFB = formData.get("portsFB")
    tags = formData.get("tags")
    
    if portsFB:
        portsFB = portsFB.split(",")
    if tags:
        tags = tags.split(",")

    # check if ipv4 exists        
    if not check_ipv4_exists(ipv4):
        # write to database
        write_to_db("host", {"name": name, "ipv4": ipv4, "ipv6": ipv6})
        # get the last host id
        host_id = check_ipv4_exists(ipv4, method="id")
        # write ports to database
        for portFB in portsFB:
            write_to_db("portFB", {"host_id": host_id, "portFB_number": portFB})
        # write tags to database
        for tag in tags:
            write_to_db("tag", {"tag_name": tag})
            tag_id = check_tag_exists(tag, method="id")
            write_to_db("host_tag", {"host_id": host_id, "tag_id": tag_id})
        db.session.commit()
    

# function which deletes the given data from the table
def delete_from_db(table, id):
    if table == "host":
        host = Host.query.filter_by(id=id).first()
        host.deleted = True
    elif table == "port":
        port = Port.query.filter_by(id=id).first()
        db.session.delete(port)
    elif table == "tag":
        tag = Tag.query.filter_by(id=id).first()
        tag.deleted = True
    elif table == "host_tag":
        host_id, tag_id = id.split("_")
        host_tag = HostTag.query.filter_by(host_id=host_id, tag_id=tag_id).first()
        db.session.delete(host_tag)
    elif table == "portFB":
        portFB = PortFB.query.filter_by(id=id).first()
        db.session.delete(portFB)
    else:
        print("Error: table not found")
        
# function which deletes an host from the table by the given id
def delete_host_by_id(id):
    host = get_host_by_id(id)
    portsFB = host["portsFB"]
    tags = host["tags"]
    
    print("Deleting host with ID:", id)
    delete_from_db("host", id)    
    for portFB in portsFB:
        portFBID = check_portFB_exists(portFB, method="id")
        print("Deleting portFB with ID:", portFBID)
        delete_from_db("portFB", portFBID)
    for tag in tags:
        tagID = check_tag_exists(tag, method="id")
        print("Deleting host_tag with ID:", tagID)
    # delete host_tag
    for tag in tags:
        tagID = check_tag_exists(tag, method="id")
        print("Deleting host_tag with ID:", id, tagID)
        delete_from_db("host_tag", f"{id}_{tagID}")
    print("Host with id: ", id, " deleted")
    db.session.commit()
    
#deletes the portsFB from one host
def delete_portsFB_by_host_id(id):
    host = get_host_by_id(id)
    portsFB = host["portsFB"]
    for portFB in portsFB:
        portFBID = check_portFB_exists(portFB, method="id")
        print("Deleting portFB with ID:", portFBID)
        delete_from_db("portFB", portFBID)
    db.session.commit() 
    
#deletes the tags from one host
def delete_tags_by_host_id(id):
    host = get_host_by_id(id)
    tags = host["tags"]
    for tag in tags:
        tagID = check_tag_exists(tag, method="id")
        print("Deleting host_tag with ID:", id, tagID)
        delete_from_db("host_tag", f"{id}_{tagID}")
    db.session.commit()

# function which updates the given data in the table
def edit_db(table, data):
    if table == "host":
        host = Host.query.filter_by(id=data["id"]).first()
        host.hostname = data["name"]
        host.ipv4 = data["ipv4"]
        host.ipv6 = data["ipv6"]
    elif table == "port":
        port = Port.query.filter_by(id=data["id"]).first()
        port.port_number = data["port_number"]
    elif table == "tag":
        tag = Tag.query.filter_by(id=data["id"]).first()
        tag.tag_name = data["tag_name"]
    elif table == "host_tag":
        host_tag = HostTag.query.filter_by(id=data["id"]).first()
        host_tag.host_id = data["host_id"]
        host_tag.tag_id = data["tag_id"]
    elif table == "portFB":
        portFB = PortFB.query.filter_by(id=data["id"]).first()
        portFB.portFB_number = data["portFB_number"]
    else:
        print("Error: table not found")

# function which writes the edits to the db
def write_edit_db(formData):
    try:
        id = formData.get("id")
        name = formData.get("name")
        tags = formData.get("tags")
        ipv4 = formData.get("ipv4")
        ipv6 = formData.get("ipv6")
        portsFB = formData.get("portsFB")
        tags = formData.get("tags")
        print("ID:", id, "Name:", name, "Tags:", tags, "IPv4:", ipv4, "IPv6:", ipv6, "PortsFB:", portsFB)
        
    
        edit_db("host", {"id": id, "name": name, "ipv4": ipv4, "ipv6": ipv6})
        # firstly delete all ports which are in the db for the host then add the new ones
        delete_portsFB_by_host_id(id)
        for portFB in portsFB:
            print("PortFB:", portFB)
            portFBID = check_portFB_exists(portFB, method="id")
            if portFBID:
                print("Port ", portFB, " gibt es schon")
            else:
                write_to_db("portFB", {"host_id": id, "portFB_number": portFB})
        # delete all tags which are in the db for the host then add the new ones
        delete_tags_by_host_id(id)
        for tag in tags:
            print("Tag:", tag)
            tagID = check_tag_exists(tag, method="id")
            if tagID:
                write_to_db("host_tag", {"host_id": id, "tag_id": tagID})
            else:
                write_to_db("tag", {"tag_name": tag})
                tagID = check_tag_exists(tag, method="id")
                write_to_db("host_tag", {"host_id": id, "tag_id": tagID})
        db.session.commit()
        return True
    except Exception as e:
        print("Error:", e)
        db.session.rollback()
        return False

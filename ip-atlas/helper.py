import json
import os
import platform
import subprocess
from models import Host, Port, Tag
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import atlasapp

DATABASE_URI = atlasapp.config["SQLALCHEMY_DATABASE_URI"]
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

#! db functions

# function which checks if the given tag exists in the database and returns the id if it exists
def tag_exists(tag_name, method="bool"):
    session = Session()
    tag = session.query(Tag).filter_by(tag_name=tag_name).first()
    session.close()
    if method == "id":
        if tag:
            return tag.id
        else:
            return None
    else:
        return tag is not None


# checks if the json document is there
def checkJson():
    if checkDokument(gPath):
        return True
    else:
        return False


# checks if the json is empty
# open the file and if the content is {} then it is empty


def checkJsonEmpty():
    if os.path.exists(gPath):
        with open(gPath) as f:
            data = json.load(f)
            f.close()
            if data == {}:
                return True
            else:
                return False


# simply creates the json document


def createJson():
    if not checkJson():
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(gPath), exist_ok=True)
        with open(gPath, "w") as f:
            f.write("{}")
            f.close()
    else:
        print("Json document already exists")


#! json use functions

# this function will be used to load the json document


def loadJson():
    with open(gPath) as f:
        data = json.load(f)
        f.close()
        return data


# this function will be used to save the json document


def saveJson(data):
    with open(gPath, "w") as f:
        json.dump(data, f)
        f.close()


# this function will be used to add a new host inclusive an running id, his name, the ip, the openend ports to the json document


def writeJson(name, ip, tags, ipv6, ports):
    data = loadJson()
    if checkJsonEmpty():
        data["hosts"] = []
        data["hosts"].append(
            {
                "id": 1,
                "name": name,
                "tags": tags,
                "ip": ip,
                "ipv6": ipv6,
                "ports": ports,
            }
        )
        saveJson(data)
    else:
        data["hosts"].append(
            {
                "id": len(data["hosts"]) + 1,
                "name": name,
                "tags": tags,
                "ip": ip,
                "ipv6": ipv6,
                "ports": ports,
            }
        )
        saveJson(data)


# this function will be used to delete a host from the json document


def deleteHost(id):
    ports = []
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                # write the host to the trash json document
                writeTrashJson(
                    data["hosts"][i]["name"],
                    data["hosts"][i]["ip"],
                    data["hosts"][i]["tags"],
                    data["hosts"][i]["ipv6"],
                    data["hosts"][i]["ports"],
                )
                del data["hosts"][i]
                saveJson(data)
                break
    else:
        print("Json document is empty")


# this function will be used to update a host in the json document


def updateJson(id, name, tags, ip, ipv6, ports):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                data["hosts"][i]["name"] = name
                data["hosts"][i]["tags"] = tags
                data["hosts"][i]["ip"] = ip
                data["hosts"][i]["ipv6"] = ipv6
                data["hosts"][i]["ports"] = ports
                saveJson(data)
                break
    else:
        print("Json document is empty")


# this function will be used to get the host by id


def getHostById(id):
    data = loadJson()
    # cut spaces from the front and from the back of the id
    # id = id.strip()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                print("Daten der ID: ", id, " :", data["hosts"][i])
                return data["hosts"][i]
            else:
                print("Host with id: ", id, " not found")
    else:
        print("Json document is empty")


def updateIpAddressById(id, data):
    jsonData = loadJson()
    if not checkJsonEmpty():
        for i, host in enumerate(jsonData["hosts"]):
            if host["id"] == id:
                # Convert ports to integers if they are not already
                if "ports" in data:
                    data["ports"] = [
                        int(port) if isinstance(port, str) and port.isdigit() else port
                        for port in data["ports"]
                    ]

                # Ensure tags are a list if not already
                if "tags" in data and isinstance(data["tags"], str):
                    data["tags"] = [tag.strip() for tag in data["tags"].split(",")]

                jsonData["hosts"][i].update(data)
                saveJson(jsonData)
                print(f"Host with id: {id} updated successfully.")
                return True
        print(f"Host with id: {id} not found.")
        return False
    else:
        print("JSON document is empty.")
        return False


#! trash json

# will check if the trash json document exists


def checkTrashJson():
    if checkDokument(gTrashPath):
        return True
    else:
        return False


# will check if the trash json document is empty


def checkTrashJsonEmpty():
    if os.path.exists(gTrashPath):
        with open(gTrashPath) as f:
            data = json.load(f)
            f.close()
            if data == {}:
                return True
            else:
                return False


# will create the trash json document


def createTrashJson():
    if not checkTrashJson():
        os.makedirs(os.path.dirname(gTrashPath), exist_ok=True)
        with open(gTrashPath, "w") as f:
            f.write("{}")
            f.close()
    else:
        print("Trash Json document already exists")


# will load the trash json document


def loadTrashJson():
    with open(gTrashPath) as f:
        data = json.load(f)
        f.close()
        return data


# will save the trash json document


def saveTrashJson(data):
    with open(gTrashPath, "w") as f:
        json.dump(data, f)
        f.close()


# will write the host to the trash json document


def writeTrashJson(name, ip, tags, ipv6, ports):
    data = loadTrashJson()
    if checkTrashJsonEmpty():
        data["hosts"] = []
        data["hosts"].append(
            {
                "id": 1,
                "name": name,
                "tags": tags,
                "ip": ip,
                "ipv6": ipv6,
                "ports": ports,
            }
        )
        saveTrashJson(data)
    else:
        data["hosts"].append(
            {
                "id": len(data["hosts"]) + 1,
                "name": name,
                "tags": tags,
                "ip": ip,
                "ipv6": ipv6,
                "ports": ports,
            }
        )
        saveTrashJson(data)


# will delete the host from the trash json document


def deleteTrashHost(id):
    data = loadTrashJson()
    if not checkTrashJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                # write it back to the json document
                writeJson(
                    data["hosts"][i]["name"],
                    data["hosts"][i]["ip"],
                    data["hosts"][i]["tags"],
                    data["hosts"][i]["ipv6"],
                    data["hosts"][i]["ports"],
                )
                del data["hosts"][i]
                saveTrashJson(data)
                break
    else:
        print("Trash Json document is empty")


# will update the host in the trash json document


def updateTrashJson(id, name, tags, ip, ipv6, ports):
    data = loadTrashJson()
    if not checkTrashJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                data["hosts"][i]["name"] = name
                data["hosts"][i]["tags"] = tags
                data["hosts"][i]["ip"] = ip
                data["hosts"][i]["ipv6"] = ipv6
                data["hosts"][i]["ports"] = ports
                saveTrashJson(data)
                break
    else:
        print("Trash Json document is empty")


# will get the host by id from the trash json document


def getTrashHostById(id):
    data = loadTrashJson()
    if not checkTrashJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                print("Daten der ID: ", id, " :", data["hosts"][i])
                return data["hosts"][i]
            else:
                print("Host with id: ", id, " not found")
    else:
        print("Trash Json document is empty")


#! logging functions


# create a log file
def createLogFile():
    if not checkLogFile():
        with open(gLogPath, "w") as f:
            f.write("")
            f.close()


# check if there is a log file


def checkLogFile():
    if os.path.exists(gLogPath):
        return True
    else:
        return False


# write to the log file


# read the log file


#! test functions


# prints the json document
def printJson():
    data = loadJson()
    if not checkJsonEmpty():
        print(data)
    else:
        print("Json document is empty")


# check if dokument exists
def checkDokument(path):
    if os.path.exists(path):
        return True
    else:
        return False


# this function will be used to get the operating system
def getOS():
    if platform.system() == "Windows":
        return "\\"
    elif platform.system() == "Linux":
        return "/"


# this function will be used to get the root directory of the project


def getRootDirectory():
    path = os.path.abspath(__file__)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    return rootPath


#! small helper functions


def devideIp(ip):
    ip = ip.split(".")
    ip = [str(x) for x in ip]
    return ip


def checkIfInputIsNone(input):
    if input == None or input == "":
        return True
    else:
        return False


#! Leons mist
# Function to check if an IP address is pingable


def isIpPingable(ip_address):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-W", "1", ip_address]
    return (
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        == 0
    )


#! variable Section
global gpath
gPath = getRootDirectory() + getOS() + "data" + getOS() + "host.json"
gLogPath = getRootDirectory() + getOS() + "log" + getOS() + "log.txt"
gTrashPath = getRootDirectory() + getOS() + "data" + getOS() + "trash.json"


# data = getHostById(1)
# print(data)
# deleteHost(3)

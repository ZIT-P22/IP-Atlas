import json
import os
import platform
import subprocess
from models import Host, Port, Tag, PortFB


#! db functions

# function which checks if the given tag exists in the database and returns the id if it exists
def check_tag_exists(tag_name, method="bool"):
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    if method == "id":
        if tag:
            return tag.id
        else:
            return None
    else:
        return tag is not None
    

# check if the given portFB exists in the database
def check_portFB_exists(portFB_number, method="bool"):
    portFB = PortFB.query.filter_by(portFB_number=portFB_number).first()
    if method == "id":
        if portFB:
            return portFB.id
        else:
            return None
    elif method == "bool":
        return portFB is not None
    else:
        print("Error: Method not found")



# check if the given ipv4 already exists in the database
def check_ipv4_exists(ipv4 ,method="bool"):
    host = Host.query.filter_by(ipv4=ipv4).first()
    if method == "id":
        if host:
            return host.id
        else:
            return None
    elif method == "bool":
        return host is not None
    else:
        print("Error: Method not found")


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

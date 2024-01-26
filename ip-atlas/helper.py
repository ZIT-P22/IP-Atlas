import json
import os
import platform
import subprocess


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
        os.makedirs(os.path.dirname(gPath), exist_ok=True)  # Create the directory if it doesn't exist
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
def writeJson(name, ip, ipv6, ports):
    data = loadJson()
    if checkJsonEmpty():
        data["hosts"] = []
        data["hosts"].append({
            "id": 1,
            "name": name,
            "ip": ip,
            "ipv6": ipv6,
            "ports": [ports]  
        })
        saveJson(data)
    else:
        data["hosts"].append({
            "id": len(data["hosts"]) + 1,
            "name": name,
            "ip": ip,
            "ipv6": ipv6,
            "ports": [ports]  
        })
        saveJson(data)

# this function will be used to delete a host from the json document
def deleteHost(id):
    data = loadJson()     
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                del data["hosts"][i]
                saveJson(data)
                break
    else:
        print("Json document is empty")

# this function will be used to update a host in the json document
def updateJson(id, name, ip, ipv6, ports):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                data["hosts"][i]["name"] = name
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



# this function will be used to get the host by name
def getHostByName(name):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["name"] == name:
                return data["hosts"][i]
    else:
        print("Json document is empty")

# this function will be used to get the host by ip
def getHostByIp(ip):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["ip"] == ip:
                return data["hosts"][i]
    else:
        print("Json document is empty")

# this function will be used to get the host by ipv6
def getHostByIpv6(ipv6):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["ipv6"] == ipv6:
                return data["hosts"][i]
    else:
        print("Json document is empty")

# this function will be used to get the host by port
def getHostByPort(port):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if port in data["hosts"][i]["ports"]:
                return data["hosts"][i]
    else:
        print("Json document is empty")


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
    
#! variable Section
global gpath
gPath = getRootDirectory() + getOS() + "data" + getOS() + "host.json"



# data = getHostById(1)
# print(data)
# deleteHost(3)

# test the functions
# writeJson("Host1", "192.168.0.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334", [80, 443])
# writeJson("Host2", "192.168.0.2", "2001:0db8:85a3:0000:0000:8a2e:0370:7335", [22, 8080])


# Function to check if an IP address is pingable
def is_ip_pingable(ip_address):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', '-W', '1', ip_address]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

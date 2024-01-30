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
def writeJson(name, ip, tags, ipv6, ports):
    data = loadJson()
    if checkJsonEmpty():
        data["hosts"] = []
        data["hosts"].append({
            "id": 1,
            "name": name,
            "tags": [tags],
            "ip": ip,
            "ipv6": ipv6,
            "ports": [ports]  
        })
        saveJson(data)
    else:
        data["hosts"].append({
            "id": len(data["hosts"]) + 1,
            "name": name,
            "tags": [tags],
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
def updateJson(id, name, tags, ip, ipv6, ports):
    data = loadJson()
    if not checkJsonEmpty():
        for i in range(len(data["hosts"])):
            if data["hosts"][i]["id"] == id:
                data["hosts"][i]["name"] = name
                data["hosts"][i]["tags"]= tags
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

#! variable Section
global gpath
gPath = getRootDirectory() + getOS() + "data" + getOS() + "host.json"



# data = getHostById(1)
# print(data)
# deleteHost(3)

# test the functions
# writeJson("Host1", "192.168.0.1", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7334", [80, 443])
# writeJson("Host2", "192.168.0.2", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7335", [22, 8080])
# writeJson("Host3", "192.168.0.3", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7336", [8080, 9090])
# writeJson("Host4", "192.168.0.4", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7337", [443, 8081])
# writeJson("Host5", "192.168.0.5", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7338", [22, 80])
# writeJson("Host6", "192.168.0.6", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7339", [8080, 8443])
# writeJson("Host7", "192.168.0.7", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7340", [21, 587])
# writeJson("Host8", "192.168.0.8", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7341", [8080, 9091])
# writeJson("Host9", "192.168.0.9", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7342", [80, 443])
# writeJson("Host10", "192.168.0.10", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7343", [22, 8080])
# writeJson("Host11", "192.168.0.11", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7344", [8081, 9090])
# writeJson("Host12", "192.168.0.12", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7345", [80, 8443])
# writeJson("Host13", "192.168.0.13", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7346", [21, 587])
# writeJson("Host14", "192.168.0.14", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7347", [8080, 9091])
# writeJson("Host15", "192.168.0.15", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7348", [80, 443])
# writeJson("Host16", "192.168.0.16", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7349", [22, 8080])
# writeJson("Host17", "192.168.0.17", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7350", [8080, 9090])
# writeJson("Host18", "192.168.0.18", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7351", [443, 8081])
# writeJson("Host19", "192.168.0.19", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7352", [22, 80])
# writeJson("Host20", "192.168.0.20", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7353", [8080, 8443])
# writeJson("Host21", "192.168.0.21", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7354", [21, 587])
# writeJson("Host22", "192.168.0.22", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7355", [8080, 9091])
# writeJson("Host23", "192.168.0.23", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7356", [80, 443])
# writeJson("Host24", "192.168.0.24", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7357", [22, 8080])
# writeJson("Host25", "192.168.0.25", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7358", [8081, 9090])
# writeJson("Host26", "192.168.0.26", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7359", [80, 8443])
# writeJson("Host27", "192.168.0.27", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7360", [21, 587])
# writeJson("Host28", "192.168.0.28", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7361", [8080, 9091])
# writeJson("Host29", "192.168.0.29", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7362", [80, 443])
# writeJson("Host30", "192.168.0.30", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7363", [22, 8080])
# writeJson("Host31", "192.168.0.31", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7364", [8080, 9090])
# writeJson("Host32", "192.168.0.32", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7365", [443, 8081])
# writeJson("Host33", "192.168.0.33", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7366", [22, 80])
# writeJson("Host34", "192.168.0.34", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7367", [8080, 8443])
# writeJson("Host35", "192.168.0.35", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7368", [21, 587])
# writeJson("Host36", "192.168.0.36", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7369", [8080, 9091])
# writeJson("Host37", "192.168.0.37", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7370", [80, 443])
# writeJson("Host38", "192.168.0.38", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7371", [22, 8080])
# writeJson("Host39", "192.168.0.39", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7372", [8081, 9090])
# writeJson("Host40", "192.168.0.40", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7373", [80, 8443])
# writeJson("Host41", "192.168.0.41", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7374", [21, 587])
# writeJson("Host42", "192.168.0.42", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7375", [8080, 9091])
# writeJson("Host43", "192.168.0.43", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7376", [80, 443])
# writeJson("Host44", "192.168.0.44", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7377", [22, 8080])
# writeJson("Host45", "192.168.0.45", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7378", [8080, 9090])
# writeJson("Host46", "192.168.0.46", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7379", [443, 8081])
# writeJson("Host47", "192.168.0.47", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7380", [22, 80])
# writeJson("Host48", "192.168.0.48", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7381", [8080, 8443])
# writeJson("Host49", "192.168.0.49", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7382", [21, 587])
# writeJson("Host50", "192.168.0.50", "test", "2001:0db8:85a3:0000:0000:8a2e:0370:7383", [8080, 9091])


# Function to check if an IP address is pingable
def isIpPingable(ip_address):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', '-W', '1', ip_address]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

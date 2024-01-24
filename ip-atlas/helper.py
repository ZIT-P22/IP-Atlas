import json
import os
import platform

# if there is no json document this function will triggerd and create a new one
# the json document will be used to store the name + ip address + opened ports of an host
# it will stored at the root directory of the project in a folder called "data"
def createJson():
    if checkDokument(gPath) == False:
        with open(gPath, 'w') as f:
            json.dump([], f)
            f.close()
            
# this function will be used to load the json document
def loadJson():
    with open(gPath) as f:
        data = json.load(f)
        f.close()
        return data

    

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
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    return rootPath
    
#! variable Section
global gpath
gPath = getRootDirectory() + getOS() + "data" + getOS() + "host.json"


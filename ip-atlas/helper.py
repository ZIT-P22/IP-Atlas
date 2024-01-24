import json
import os
import platform


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
    path = os.path.abspath(__file__)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    return rootPath
    
#! variable Section
global gpath
gPath = getRootDirectory() + getOS() + "data" + getOS() + "host.json"

# test the functions
createJson()
print(checkJsonEmpty())
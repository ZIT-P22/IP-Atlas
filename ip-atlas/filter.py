from helper import *

#! filter functions

# this function filter the json document for any ip address which maches the pattern
# example filter could be *.168.*.2 (* menas it can be any number)
def filterByIp(octed1, octed2, octed3, octed4, data):
    if not checkJsonEmpty():
        for x in data["hosts"]:
            if not checkIfInputIsNone(octed1):
                data = [x for x in data["hosts"] if devideIp(x["ip"])[0] == int(octed1)]
            if not checkIfInputIsNone(octed2):
                data = [x for x in data if devideIp(x["ip"])[1] == octed2]
            if not checkIfInputIsNone(octed3):
                data = [x for x in data if devideIp(x["ip"])[2] == octed3]
            if not checkIfInputIsNone(octed4):
                data = [x for x in data if devideIp(x["ip"])[3] == octed4]
        return data
    else:
        print("Json document is empty")

# filter by name/name section
def filterByName(name, data):
    if not checkJsonEmpty():
        if not checkIfInputIsNone(name):
            data = [x for x in data["hosts"] if name in x["name"]]
        return data
    else:
        print("Json document is empty")
# filter by ports

# filter by tags

# filter by ipv6

# applies all filters




#! tests
print(filterByIp("192", "168", "0", "", loadJson()))
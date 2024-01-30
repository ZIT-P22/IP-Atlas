from helper import *

#! filter functions


# this function filter the json document for any ip address which maches the pattern
# example filter could be *.168.*.2 (* menas it can be any number)
#? inputs have to be strings
def filterByIp(octed1, octed2, octed3, octed4, data):
    # convert all octeds to int
    result = []
    for i in range(len(data["hosts"])):
        ip = devideIp(data["hosts"][i]["ip"])
        # print(ip[0], ip[1], ip[2], ip[3])
        # print("Oktet 1:",octed1,"Oktet 2:",octed2,"Oktet 3:",octed3,"Oktet 4:",octed4)
        if (
            (octed1 == "*" or ip[0] == octed1)
            and (octed2 == "*" or ip[1] == octed2)
            and (octed3 == "*" or ip[2] == octed3)
            and (octed4 == "*" or ip[3] == octed4)
        ):
            result.append(data["hosts"][i])
    return result


# filter by name/name section
def filterByName(search, data):
    result = []
    for i in range(len(data["hosts"])):
        dataName = data["hosts"][i]["name"]
        if search in dataName:
            result.append(data["hosts"][i])
    return result

# filter by ports
def filterByPort(search, data):
    result = []
    for host in data["hosts"]:
        dataPorts = host.get("ports")  # Use get() to handle missing "ports" key
        for port in dataPorts:
            print(port)
            print(search)
            print(dataPorts)
            for p in port:
                if search in p:
                    result.append(host)
    return result


# filter by tags

# filter by ipv6

# applies all filters


#! tests
# print(filterByIp("*", "*", "*", 12, loadJson()))
# print(filterByName("40", loadJson()))
print(filterByPort(80, loadJson()))

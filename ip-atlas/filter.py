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
    for name in data:
        dataName = name.get("name")
        if search in dataName:
            result.append(name)
    return result

# filter by ports
def filterByPort(search, data):
    result = []
    for host in data:
        dataPorts = host.get("ports")
        for port in dataPorts:
            # print(port)
            # print(search)
            # print(dataPorts)
            if search in port:
                result.append(host)
                break
    return result


# filter by tags
def filterByTags(search, data):
    result = []
    for host in data:
        dataTags = host.get("tags")
        for tag in dataTags:
            if search in tag:
                result.append(host)
                break
    return result

# filter by ipv6

# applies all filters
def filterAll(ip, name, port, tag):
    result = loadJson()
    if ip != "":
        ip = devideIp(ip)
        result = filterByIp(ip[0], ip[1], ip[2], ip[3], result)
    if name != "":
        result = filterByName(name, result)
    if port != "":
        result = filterByPort(port, result)
    if tag != "":
        result = filterByTags(tag, result)
    return result


#! tests
# print(filterByIp("*", "*", "*", "47", loadJson()))
# print(filterByName("40", loadJson()))
# data = filterByPort(99, loadJson())
# print(data)
# print(len(data))
# tags = filterByTags("tea", loadJson())
# print(tags)
# print(len(tags))
# print(filterAll("*.*.*.*", "", 80, ""))
# print(filterByIp("*", "*", "*", "*", filterByName("40", loadJson())))
# print(filterByIp("*", "*", "*", "*", filterByPort("99", loadJson())))
# printJson()
# print(filterByTags("test", filterByIp("*", "*", "*", "49", loadJson())))
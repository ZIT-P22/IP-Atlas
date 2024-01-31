from helper import *

#! filter functions


# this function filter the json document for any ip address which maches the pattern
# example filter could be *.168.*.2 (* menas it can be any number)
# ? inputs have to be strings
def filter_data(search, key, data):
    """
    Adjusted function to filter data based on the search term and key.
    Tries to match exactly first, then falls back to partial matches.
    Now performs case-insensitive matching.
    """
    search = search.lower()  # Convert search term to lowercase for case-insensitive comparison
    filtered_data = []
    if key == "ip":
        filtered_data = [host for host in data["hosts"]
                         if host["ip"].lower() == search]
    elif key == "name":
        filtered_data = [host for host in data["hosts"]
                         if host.get("name", "").lower() == search]
    elif key == "port":
        filtered_data = [host for host in data["hosts"] if search.isdigit() and int(
            search) in host.get("ports", [[]])[0]]
    elif key == "tag":
        filtered_data = [host for host in data["hosts"]
                         if search in [tag.lower() for tag in host.get("tags", [[]])[0]]]

    # If no exact matches found, revert to partial matches
    if not filtered_data:
        if key == "ip":
            filtered_data = [host for host in data["hosts"]
                             if search in host["ip"].lower()]
        elif key == "name":
            filtered_data = [host for host in data["hosts"]
                             if search in host.get("name", "").lower()]
        elif key == "port":
            # Assuming 'port' search needs to be exact; partial match fallback might not make sense here
            pass  # Already handled above with exact match logic
        elif key == "tag":
            filtered_data = [host for host in data["hosts"] if any(
                search in tag.lower() for tag in host.get("tags", [[]])[0])]

    return filtered_data



# this function filter the json document for any ip address which maches the pattern
# example filter could be *.168.*.2 (* means it can be any number)
#? inputs have to be strings
def filterByIp(octed1, octed2, octed3, octed4, data):
    # convert all octeds to int
    result = {"hosts": []}
    for i in range(len(data["hosts"])):
        ip = devideIp(data["hosts"][i]["ip"])
        if (
            (octed1 == "*" or ip[0] == octed1)
            and (octed2 == "*" or ip[1] == octed2)
            and (octed3 == "*" or ip[2] == octed3)
            and (octed4 == "*" or ip[3] == octed4)
        ):
            result["hosts"].append(data["hosts"][i])
    return result

# filter by name/name section
def filterByName(search, data):
    result = {"hosts" : []}
    # for name in data["hosts"]:
    for i in range(len(data["hosts"])):
        dataName = data["hosts"][i]["name"]
        if search in dataName:
            result["hosts"].append(data["hosts"][i])
    return result

# filter by ports
def filterByPort(search, data):
    result = {"hosts" : []}
    # for host in data:
    if not search == "":
        for i in range(len(data["hosts"])):
            # dataPorts = host.get("ports")
            dataPorts = data["hosts"][i]["ports"]
            for port in dataPorts:
            # for port in dataPorts[0]:
                # print(port)
                # print(search)
                # print(dataPorts)
                if search in port:
                    # result.append(host)
                    result["hosts"].append(data["hosts"][i])
                    break
        return result
    else:
        return data


# filter by tags
def filterByTags(search, data):
    result = {"hosts" : []}
    # for host in data:
    for i in range(len(data["hosts"])):
        # dataTags = host.get("tags")
        dataTags = data["hosts"][i]["tags"]
        for tag in dataTags:
            if search in tag:
                # result.append(host)
                result["hosts"].append(data["hosts"][i])
                break
    return result

# applies all filters
def filterAll(ip, name, port, tag, data):
    result = data
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
# print(filterAll("*.*.*.*", "", "", ""))
print(filterByIp("*", "*", "*", "*", filterByName("", filterByPort("", filterByTags("tea", loadJson())))))
# print(filterByIp("*", "*", "*", "*", filterByPort("99", loadJson())))
# printJson()
# print(filterByTags("test", filterByIp("*", "*", "*", "49", loadJson())))

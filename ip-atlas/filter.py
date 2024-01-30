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


def filter_all(ip="", name="", port="", tag=""):
    """
    Applies all filters based on the provided search criteria.
    """
    data = loadjson()
    if ip:
        data["hosts"] = filter_data(ip, "ip", data)
    if name:
        data["hosts"] = filter_data(name, "name", data)
    if port:
        data["hosts"] = filter_data(port, "port", data)
    if tag:
        data["hosts"] = filter_data(tag, "tag", data)
    return data


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

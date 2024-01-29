from helper import *

#! filter functions

# this function filter the json document for any ip address which maches the pattern
# example filter could be *.168.*.2 (* menas it can be any number)
def filterByIp(octed1, octed2, octed3, octed4, data):
    # convert all octeds to int
    result = []
    for i in range(len(data["hosts"])):
        ip = devideIp(data["hosts"][i]["ip"])
        # print(ip)
        # print("Oktet 1:",octed1,"Oktet 2:",octed2,"Oktet 3:",octed3,"Oktet 4:",octed4)
        if ip[0] == octed1 or octed1 == "*":
            if ip[1] == octed2 or octed2 == "*":
                if ip[2] == octed3 or octed3 == "*":
                    if ip[3] == octed4 or octed4 == "*":
                        result.append(data["hosts"][i])
                        print(data["hosts"][i]["ip"])


# filter by name/name section

# filter by ports

# filter by tags

# filter by ipv6

# applies all filters




#! tests
print(filterByIp("192", "*", "*", "*", loadJson()))

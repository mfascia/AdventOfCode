import sys
import re
import json

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(input_stream):
    bots = {}
    outputs = {}

    input_stream.sort()

    for line in input_stream:
        if line[:5] == "value":
            groups = re.match("value ([0-9]*) goes to bot ([0-9]*)", line).groups()
            if len(groups):
                params = map(lambda x: int(x), groups)
                if bots.has_key(params[1]):
                    bots[params[1]]["values"].append(params[0])
                    bots[params[1]]["values"].sort()
                else:
                    bots[params[1]] = {
                        "values": [params[0]],
                        "rules": [0, 0]
                    }

    for line in input_stream:
        if line[:5] != "value":
            groups = re.match("bot ([0-9]*) gives low to (bot|output) ([0-9]*) and high to (bot|output) ([0-9]*)", line).groups()
            if len(groups):
                s = int(groups[0])
                d1 = int(groups[2]) * (1 if groups[1] == "bot" else -1)
                d2 = int(groups[4]) * (1 if groups[3] == "bot" else -1)
                if bots.has_key(s):
                    bots[s]["rules"] = [d1, d2]
                else:
                    bots[s] = {
                        "values": [],
                        "rules": [d1, d2]
                    }

    propagate = True
    step = 0
    while propagate:
        propagate = False
        for item in bots.iteritems():
            if len(item[1]["values"]) == 2:
                print step, item
                if item[1]["rules"][0] > 0:
                    bots[item[1]["rules"][0]]["values"].append(item[1]["values"][0])
                    bots[item[1]["rules"][0]]["values"].sort()
                    if bots[item[1]["rules"][0]]["values"] == [17, 61]:
                        print item
                        break
                else:
                    outputs[-1 * item[1]["rules"][0]] = item[1]["values"][0]

                if item[1]["rules"][1] > 0:
                    bots[item[1]["rules"][1]]["values"].append(item[1]["values"][1])
                    bots[item[1]["rules"][1]]["values"].sort()
                    if bots[item[1]["rules"][1]]["values"] == [17, 61]:
                        print item
                        break
                else:
                    outputs[-1 * item[1]["rules"][1]] = item[1]["values"][1]
                item[1]["values"] = []
                propagate = True
        step += 1

    # print json.dumps(bots, indent=4, sort_keys=True)
    # print json.dumps(outputs, indent=4, sort_keys=True)
                
                
            

def main_2(input_stream):
    pass


if __name__ == "__main__":
    input_stream = read_input_stream("AoC_10_input.txt")
    main_1(input_stream)
    print
    main_2(input_stream)


'''
'''
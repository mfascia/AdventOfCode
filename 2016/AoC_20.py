import sys


def read_input(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main(text):
    mins = []
    maxs = []
    for line in text:
        interval = [int(x) for x in line.split("-")]
        mins.append(interval[0])
        maxs.append(interval[1])
    
    mins.sort()
    maxs.sort()

    if mins[0] > 0:
        return 0

    nb_allowed = 0
    first_allowed = -1
    i = 0
    j = 0
    s = 0
    while i<len(mins) and j<len(maxs):
        if mins[i] < maxs[j]:
            s += 1
            i += 1
        elif mins[i] > maxs[j]:
            s -= 1
            if s == 0 and mins[i] != maxs[j]+1:
                if first_allowed == -1:
                    first_allowed = maxs[j]+1
                nb_allowed += mins[i] - (maxs[j]+1) 
            j += 1

    print "part 1 - first allowed:", first_allowed
    print "part 2 - nb allowed:", nb_allowed


def main_2(text):
    pass


if __name__ == "__main__":
    text = read_input("AoC_20_input.txt")
    main(text)


'''
--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later. However, the corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written as plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7

The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed. Then, the only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that is not blocked?

Your puzzle answer was 32259706.
--- Part Two ---

How many IPs are allowed by the blacklist?

Your puzzle answer was 113.
'''
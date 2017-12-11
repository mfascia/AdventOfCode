import sys
import math
import cmath

# Good resource on hex grids: https://www.redblobgames.com/grids/hexagons/

unit = {
    "n":  [ 0,  1, -1],
    "ne": [ 1,  0, -1],
    "se": [ 1, -1,  0],
    "s":  [ 0, -1,  1],
    "sw": [-1,  0,  1],
    "nw": [-1,  1,  0]
}

hex_origin = [0, 0, 0]


def hex_add(a, b):
    return [x+y for x,y in zip(a,b)]


def hex_dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def part1(inp):
    pos = hex_origin
    for i in inp:
        pos = hex_add(pos, unit[i])
    print hex_dist(pos, hex_origin)


def part2(inp):
    f = 0
    pos = hex_origin
    for i in inp:
        pos = hex_add(pos, unit[i])
        d = hex_dist(pos, hex_origin)
        if d > f:
            f = d
    print f


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


if __name__ == "__main__":
    
    inp = ""
    if len(inp) == 0:
        inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))[0].split(",")

    print "--------------------------------------"
    print "- 1:"
    print "--------------------------------------"
    part1(inp)

    print "--------------------------------------"
    print "- 2:"
    print "--------------------------------------"
    part2(inp)

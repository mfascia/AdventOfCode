import os
import sys


def main_1(inp):
    print "Part 1:"
    layers = {}
    for line in inp:
        layer, depth = [int(x) for x in line.split(": ")]
        layers[layer] = depth

    severity = 0
    for layer, depth in layers.items():
        sentinel = layer % (2*depth - 2)    # Sentinel going down and up return at pos 0 every 2.depth-2
        if sentinel == 0:
            severity += layer * depth

    print severity


def main_2(inp):
    print "Part 2:"
    layers = {}
    for line in inp:
        layer, depth = [int(x) for x in line.split(": ")]
        layers[layer] = depth

    delay = 0
    while True:
        severity = 0
        caught = False
        for layer, depth in layers.items():
            sentinel = (layer + delay) % (2*depth - 2)    # Sentinel going down and up return at pos 0 every 2.depth-2
            if sentinel == 0:
                caught = True
                delay += 1
                break
        if not caught:
            break

    print delay

def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


if __name__ == "__main__":
    
    # read tests
    tests = []
    if len(tests) == 0:
        i = 0
        while True:
            i += 1
            testfile = sys.argv[0].replace(".py", ("_test_%d.txt" % i))
            if os.path.isfile(testfile):
                tests.append(read_input_file(testfile))
            else:
                break

    # read input
    inp = []
    if len(inp) == 0:
        inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))

    # run tests
    print "--------------------------------------"
    print "- TESTS"
    print "--------------------------------------"
    for test in tests:
        main_1(test)
        main_2(test)
        print "---"

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        main_1(inp)
        main_2(inp)
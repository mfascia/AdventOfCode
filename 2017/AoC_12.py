import os
import sys


def main_1(inp):
    print "Part 1:"
    graph = {}
    for line in inp:
        parent, right = line.split(" <-> ")
        children = right.split(", ")
        graph[int(parent)] = [int(x) for x in children]

    visited = []
    to_visit = [0]
    while len(to_visit) > 0:
        n = to_visit.pop(0)
        if not n in visited:
            visited.append(n)
            to_visit += graph[n]
    print len(visited), visited

def main_2(inp):
    print "Part 2:"
    graph = {}
    for line in inp:
        parent, right = line.split(" <-> ")
        children = right.split(", ")
        graph[int(parent)] = [int(x) for x in children]

    in_group = [-1 for x in graph]

    group_id = 0
    for k in xrange(0, len(in_group)):
        if in_group[k] > -1:
            continue

        visited = []
        to_visit = [k]
        while len(to_visit) > 0:
            n = to_visit.pop(0)
            if not n in visited:
                visited.append(n)
                in_group[n] = group_id
                to_visit += graph[n]
        print str(group_id) + ": " + str(len(visited)), visited
        group_id += 1
    
    print group_id


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
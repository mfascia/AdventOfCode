import os
import sys

def find_start(grid):
    for i in xrange(0, len(grid[0])):
        if grid[0][i] == "|":
            return [i, 0]
    return [-1, -1]

next = {
    "s": [0, 1],
    "n": [0, -1],
    "e": [1, 0],
    "w": [-1, 0]
}


def main(grid):
    print "Part 1:"
    dir = "s"
    prev = find_start(grid)
    pos = [prev[0], prev[1]+1]
    msg = ""
    steps = 1
    while True:
        if not grid[pos[1]][pos[0]] in "-|":
            if grid[pos[1]][pos[0]] == "+":
                print pos, "found corner"
                if dir in "ns":
                    for c in "ew":
                        peek = [a+b for a,b in zip(pos, next[c])]
                        if grid[peek[1]][peek[0]] != " ":
                            dir = c
                            break
                else:
                    for c in "ns":
                        peek = [a+b for a,b in zip(pos, next[c])]
                        if grid[peek[1]][peek[0]] != " ":
                            dir = c
                            break
                    pass
            elif grid[pos[1]][pos[0]] == " ":
                print "reached the end!"
                break
            else:
                print pos, "found", grid[pos[1]][pos[0]]
                msg += grid[pos[1]][pos[0]] 
        prev = pos
        steps += 1
        pos = [a+b for a,b in zip(pos, next[dir])]
    print msg
    print steps, "steps"


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    return raw


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
    if True:
        print "--------------------------------------"
        print "- TESTS"
        print "--------------------------------------"
        for test in tests:
            main(test)
            print "---"

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        main(inp)
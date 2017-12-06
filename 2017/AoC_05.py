import sys


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: int(x.strip(" \n\t")), raw)
    return stream


def main_1(inp):
    size = len(inp)
    pc = 0
    steps = 0
    while (pc>=0) and (pc<size):
        npc = pc + inp[pc]
        inp[pc] += 1
        pc = npc
        steps += 1
    print steps


def main_2(inp):
    size = len(inp)
    pc = 0
    steps = 0
    while (pc>=0) and (pc<size):
        npc = pc + inp[pc]
        if inp[pc] >= 3:
            inp[pc] -= 1
        else:
            inp[pc] += 1
        pc = npc
        steps += 1
    print steps


if __name__ == "__main__":
    print "--------------------------------------"
    print "- 1:"
    print "--------------------------------------"
    inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))
    main_1(inp)

    print "--------------------------------------"
    print "- 2:"
    print "--------------------------------------"
    inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))
    main_2(inp)


'''
--------------------------------------
- 1:
--------------------------------------
339351
--------------------------------------
- 2:
--------------------------------------
24315397
'''
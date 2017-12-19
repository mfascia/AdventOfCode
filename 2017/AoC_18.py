import os
import sys
import re


def init_regs(pid):
    regs = {}
    for c in "abcdefghijklmnop":
        regs[c] = 0
    regs["p"] = pid
    return regs


def run(regs, prog):
    out = []
    rcv = []
    i = 0
    while i < len(prog):
        line = prog[i]
        if line.startswith("snd"):
            x = line.split(" ")[1]
            if x in "abcdefghijklmnop":
                out.append(regs[x])
            else:
                out.append(int(x))
            i += 1
        elif line.startswith("set"):
            x, y = line.split(" ")[1:]
            if y in "abcdefghijklmnop":
                regs[x] = regs[y]
            else:
                regs[x] = int(y)
            i += 1
        elif line.startswith("add"):
            x, y = line.split(" ")[1:]
            if y in "abcdefghijklmnop":
                regs[x] += regs[y]
            else:
                regs[x] += int(y)
            i += 1
        elif line.startswith("mul"):
            x, y = line.split(" ")[1:]
            if y in "abcdefghijklmnop":
                regs[x] *= regs[y]
            else:
                regs[x] *= int(y)
            i += 1
        elif line.startswith("mod"):
            x, y = line.split(" ")[1:]
            if y in "abcdefghijklmnop":
                regs[x] = regs[x] % regs[y]
            else:
                regs[x] = regs[x] % int(y)
            i += 1
        elif line.startswith("rcv"):
            x = line.split(" ")[1]
            if x in "abcdefghijklmnop":
                v = regs[x]
                if v != 0:
                    rcv.append(out[-1])
                    break    
            i += 1
        elif line.startswith("jgz"):
            x, y = line.split(" ")[1:]
            if x in "abcdefghijklmnop":
                if regs[x] > 0:
                    if y in "abcdefghijklmnop":
                        off = regs[y]
                    else:
                        off = int(y)
                    i += off
                else:
                    i += 1
            else:
                if int(x) > 0:
                    if y in "abcdefghijklmnop":
                        off = regs[y]
                    else:
                        off = int(y)
                    i += off
                else:
                    i += 1
        else:
            i += 1
    return out, rcv
               

def step(regs, prog, snd_q, rcv_q, i):
    line = prog[i]
    if line.startswith("snd"):
        x = line.split(" ")[1]
        if x in "abcdefghijklmnop":
            snd_q.append(regs[x])
        else:
            snd_q.append(int(x))
    elif line.startswith("set"):
        x, y = line.split(" ")[1:]
        if y in "abcdefghijklmnop":
            regs[x] = regs[y]
        else:
            regs[x] = int(y)
    elif line.startswith("add"):
        x, y = line.split(" ")[1:]
        if y in "abcdefghijklmnop":
            regs[x] += regs[y]
        else:
            regs[x] += int(y)
    elif line.startswith("mul"):
        x, y = line.split(" ")[1:]
        if y in "abcdefghijklmnop":
            regs[x] *= regs[y]
        else:
            regs[x] *= int(y)
    elif line.startswith("mod"):
        x, y = line.split(" ")[1:]
        if y in "abcdefghijklmnop":
            regs[x] = regs[x] % regs[y]
        else:
            regs[x] = regs[x] % int(y)
    elif line.startswith("rcv"):
        x = line.split(" ")[1]
        if len(rcv_q) > 0:
            regs[x] = rcv_q.pop(0)
        else:
            return i
    elif line.startswith("jgz"):
        x, y = line.split(" ")[1:]
        if x in "abcdefghijklmnop":
            if regs[x] > 0:
                if y in "abcdefghijklmnop":
                    off = regs[y]
                else:
                    off = int(y)
                return i + off
        else:
            if int(x) > 0:
                if y in "abcdefghijklmnop":
                    off = regs[y]
                else:
                    off = int(y)
                return i + off
    return i + 1


def main_1(inp):
    print "Part 1:"
    regs = init_regs(0)
    out, rcv = run(regs, inp)
    print out
    print rcv


def main_2(inp):
    print "Part 2:"
    regs0 = init_regs(0)
    regs1 = init_regs(1)
    q0 = []
    q1 = []
    pc0 = 0
    pc1 = 0
    snd1_count = 0
    while True:
        if pc0 < len(inp):
            npc0 = step(regs0, inp, q1, q0, pc0)
        if pc1 < len(inp):
            npc1 = step(regs1, inp, q0, q1, pc1)
            if inp[pc1].startswith("snd"):
                snd1_count += 1
        if pc0 == npc0 and pc1 == npc1:
            break
        else:
            pc0 = npc0
            pc1 = npc1
    print snd1_count


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
    if True:
        print "--------------------------------------"
        print "- TESTS"
        print "--------------------------------------"
        main_1(tests[0])
        print "---"
        main_2(tests[1])

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        main_1(inp)
        main_2(inp)
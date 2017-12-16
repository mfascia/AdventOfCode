import os
import sys


def spin(txt, i):
    return txt[-i:] + txt[:-i]


def exchange(txt, s, a, b):
    ret = ""
    for i in xrange(0, s):
        if i == a:
            ret += txt[b]
        elif i == b:
            ret += txt[a]
        else:
            ret += txt[i]
    return ret


def partner(txt, a, b):
    ret = ""
    for c in txt:
        if c == a:
            ret += b
        elif c == b:
            ret += a
        else:
            ret += c
    return ret
    


def dance(text, commands):
    for line in commands:
        for cmd in line.split(","):
            if cmd[0] == "s":
                text = spin(text, int(cmd[1:]))
            elif cmd[0] == "x":
                a,b = cmd[1:].split("/")
                text = exchange(text, 16, int(a), int(b))
            elif cmd[0] == "p":
                a,b = cmd[1:].split("/")
                text = partner(text, a, b)
    return text

def main_1(inp):
    print "Part 1:"
    print dance("abcdefghijklmnop", inp)


def main_2(inp):
    print "Part 2:"

    # try and find any periodicity in the output 
    text = "abcdefghijklmnop"
    history = []
    i = 0
    while not text in history:
        print text
        history.append(text)
        text = dance(text, inp)
        i += 1
    print text
    offset = history.index(text)
    period = i - offset
    print "Found periodic output. Period:", period, "with initial offset of", offset
    print "State after 1 billion dances:", history[(1000000000 - offset) % period]
    

def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


if __name__ == "__main__":
    
    # read tests
    tests = [
        ["s1"],
        ["x3/4"],
        ["pe/b"]
    ]   

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
            main_1(test)
            main_2(test)
            print "---"

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        main_1(inp)
        main_2(inp)
import os
import sys

# This is overall quite slow. Do not run in debugger, use command line instead!

def main_1(inp):
    print "Part 1:"
    gen = [16807, 48271]
    matches = 0
    for x in xrange(0, 40000000):
        inp = [
            (inp[0] * gen[0]) % 2147483647,
            (inp[1] * gen[1]) % 2147483647 ]
        if (inp[0] & 0xFFFF) == (inp[1] & 0xFFFF):
            matches += 1
        if x % 1000000 == 0:
            print x
    print matches


def main_2(inp):
    print "Part 2:"

    print "Gen left"

    left = []
    v = inp[0]
    while len(left) < 5000000:
        if v % 4 == 0:
            left.append(v)
        v = (v * 16807) % 2147483647
        
    print "Gen right"

    right = []
    v = inp[1]
    while len(right) < 5000000:
        if v % 8 == 0:
            right.append(v)
        v = (v * 48271) % 2147483647L

    print "Gen matches"
             
    matches = 0
    for i in xrange(0, 5000000):
        if (left[i] & 0xFFFF) == (right[i] & 0xFFFF):
            matches += 1

    print matches


if __name__ == "__main__":
    # read tests
    tests = [[65, 8921]]

    # read input
    inp = [699, 124]

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
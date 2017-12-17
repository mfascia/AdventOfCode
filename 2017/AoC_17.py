import os
import sys
from collections import deque


def print_buffer(buf, v):
    s = ""
    for i in xrange(0, len(buf)):
        if buf[i] == v:
            s += "(((((" + str(buf[i]) + "))))) "
        else:
            s += str(buf[i]) + " "
    print s


def main_1(offset, num_iter):
    print "Part 1:"
    buf = [0]
    p = 0 
    for i in xrange(1, num_iter+1):
        p = ((p + offset) % (i)) + 1
        buf.insert(p, i)

    print_buffer(buf, 2017)
    try:
        p = buf.index(2017)
        print "Item after 2017 is", buf[(p+1)%len(buf)]
    except:
        print "Item 2017 is not in buffer"


def main_2(offset, num_iter):
    print "Part 2:"
    # inserting in an array is way too slow. moving to a deque
    # buf = [0]
    # p = 0 
    # last = 0
    # for i in xrange(1, num_iter+1):
    #     p = ((p + offset) % (i)) + 1
    #     buf.insert(p, i)
    #     if buf[1] != last:
    #         print i, ":", last, "->", buf[1]
    #         last = buf[1]

    buf = deque()
    buf.append(0)
    #last = 0
    for i in xrange(1, num_iter+1):
        if i % 1000000 == 0:
            print i, "iterations..."
        buf.rotate(-offset)
        buf.append(i)
        # if buf[1] != last:
        #     print i, ":", last, "->", buf[1]
        #     last = buf[1]
    for i in xrange(0, num_iter+1):
        v = buf.popleft()
        if v == 0:
            print buf[0]
            break


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


if __name__ == "__main__":
    
    # test input
    test = 3

    # real input
    inp = 359

    print "--------------------------------------"
    print "- TESTS"
    print "--------------------------------------"
    main_1(test, 10)

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        main_1(inp, 2017)
        main_2(inp, 50000000)
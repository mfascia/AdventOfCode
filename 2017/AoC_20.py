import os
import sys
import re


def main(inp, iter, coll):
    particles = []
    for line in inp:
        matches = [int(x) for x in re.match("p=<(-?\d*),(-?\d*),(-?\d*)>, v=<(-?\d*),(-?\d*),(-?\d*)>, a=<(-?\d*),(-?\d*),(-?\d*)>", line).groups()]
        matches.append(1)
        particles.append(matches)

    nbp = len(particles)
    for t in xrange(0, iter):
        for i in xrange(0, nbp):
            p = particles[i]
            if p[9] == 1:
                # update v
                p[3] += p[6]
                p[4] += p[7]
                p[5] += p[8]
                # update p
                p[0] += p[3]
                p[1] += p[4]
                p[2] += p[5]
        if coll:
            for i in xrange(0, nbp-1):
                p1 = particles[i]
                if p1[9] == 0:
                    continue            
                for j in xrange(i+1, nbp):
                    p2 = particles[j]
                    if p2[9] == 0:
                        continue            
                    if p1[0] == p2[0] and p1[1] == p2[1] and p1[2] == p2[2]:
                        p1[9] = 0
                        p2[9] = 0

    if coll:
        alive = 0
        for i in xrange(0, len(particles)):
            p = particles[i]
            if p[9] == 1:
                alive += 1
        print alive
    else:
        min_i = -1
        min = 10000000000
        for i in xrange(0, len(particles)):
            p = particles[i]
            md = abs(p[0]) + abs(p[1]) + abs(p[2])
            if min > md:
                min_i = i
                min = md

        print min_i, "md=", min


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
        for test in tests:
            main(test, 100, False)
            main(test, 100, True)
            print "---"

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        main(inp, 1000, False)
        main(inp, 1000, True)
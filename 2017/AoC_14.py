import os
import sys


def reverse_range(buffer, pos, size):
    temp = []
    max = len(buffer)
    if pos+size > max:
        temp += buffer[pos:]
        temp += buffer[0:pos+size-max]
        rev = temp [::-1]
        buffer2 = rev[max-pos:] + buffer[pos+size-max:pos] + rev[:max-pos]
    else:
        temp = buffer[pos:pos+size]
        rev = temp[::-1]
        buffer2 = buffer[0:pos] + rev + buffer[pos+size:]
    return buffer2


def knot_hash(inp):
    buff = [i for i in xrange(0, 256)]
    skip = 0
    pos = 0
    seq = [ord(x) for x in inp] + [17, 31, 73, 47, 23]
    for loop in xrange(0, 64):
        for i in seq:
            if i > len(buff):
                continue
            buff = reverse_range(buff, pos, i)
            pos = (pos + i + skip) % len(buff)
            skip = (skip + 1) % len(buff)
    dense = []
    for a in xrange(0, len(buff)/16):
        hash = buff[16*a]
        for b in xrange(1, 16):
            hash = hash ^ buff[16*a + b]
        dense.append(hash)
    return ''.join(["%02x" % x for x in dense])


bin_lut = {
    "0": [0,0,0,0],
    "1": [0,0,0,1],
    "2": [0,0,1,0],
    "3": [0,0,1,1],
    "4": [0,1,0,0],
    "5": [0,1,0,1],
    "6": [0,1,1,0],
    "7": [0,1,1,1],
    "8": [1,0,0,0],
    "9": [1,0,0,1],
    "a": [1,0,1,0],
    "b": [1,0,1,1],
    "c": [1,1,0,0],
    "d": [1,1,0,1],
    "e": [1,1,1,0],
    "f": [1,1,1,1]
}

bin_bits = {
    "0": 0,
    "1": 1,
    "2": 1,
    "3": 2,
    "4": 1,
    "5": 2,
    "6": 2,
    "7": 3,
    "8": 1,
    "9": 2,
    "a": 2,
    "b": 3,
    "c": 2,
    "d": 3,
    "e": 3,
    "f": 4
}


def main(inp):
    count = 0
    data = [ [] for x in xrange(0, 128) ]
    for i in xrange(0, 128):
        s = inp + "-" + str(i)
        h = knot_hash(s)
        for c in h:
            data[i] += bin_lut[c]                    
            count += bin_bits[c]
    print "used: ", count
   
    regions = 0
    for y in xrange(0, 128):
        for x in xrange(0, 128):
            if data[x][y] == 1:
                to_visit = [[x, y]]
                while len(to_visit) > 0:
                    a, b = to_visit.pop(0)
                    data[a][b] = regions + 2
                    if a>0 and data[a-1][b]==1: to_visit.append([a-1, b])
                    if b>0 and data[a][b-1]==1: to_visit.append([a, b-1])
                    if a<127 and data[a+1][b]==1: to_visit.append([a+1, b])
                    if b<127 and data[a][b+1]==1: to_visit.append([a, b+1])
                regions += 1

    print "regions: ", regions    


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


if __name__ == "__main__":
    
    inp = "hfdlxzhv"

    print "--------------------------------------"
    main(inp)
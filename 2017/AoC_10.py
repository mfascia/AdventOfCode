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


def main_1(inp):
    buff = [i for i in xrange(0, 256)]
    skip = 0
    pos = 0
    for i in inp:
        if i > len(buff):
            continue
        buff = reverse_range(buff, pos, i)
        pos = (pos + i + skip) % len(buff)
        skip = (skip + 1) % len(buff)
    print str(buff[0] * buff[1])


def main_2(inp):
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
    print ''.join(["%02x" % x for x in dense])


if __name__ == "__main__":
    
    print "--------------------------------------"
    print "- 1:"
    print "--------------------------------------"
    main_1([106,118,236,1,130,0,235,254,59,205,2,87,129,25,255,118])

    print "--------------------------------------"
    print "- 2:"
    print "--------------------------------------"
    main_2("106,118,236,1,130,0,235,254,59,205,2,87,129,25,255,118")
import sys

def is_anagram(w1, w2):
    lut = {}

    for l in w1:
        if lut.has_key(l):
            lut[l] += 1
        else:
            lut[l] = 1

    for l in w2:
        if not lut.has_key(l):
            return False
        else:
            lut[l] -= 1

    for l in lut:
        if lut[l] != 0:
            return False
    return True
        

def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(inp):
    valid = 0
    for line in inp:
        nogood = False
        words = line.split(" ")
        for i in xrange(0, len(words)-1):
            for j in xrange(i+1, len(words)):
                if words[i] == words[j]:
                    nogood = True
                    break
            if nogood:
                break
        if not nogood:
            valid += 1

    print valid

def main_2(inp):
    valid = 0
    for line in inp:
        nogood = False
        words = line.split(" ")
        for i in xrange(0, len(words)-1):
            for j in xrange(i+1, len(words)):
                if is_anagram(words[i], words[j]):
                    nogood = True
                    break
            if nogood:
                break
        if not nogood:
            valid += 1

    print valid


if __name__ == "__main__":
    
    is_anagram("aaa", "abc")

    inp = ""
    if len(inp) == 0:
        inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))

    print "--------------------------------------"
    print "- 1:"
    print "--------------------------------------"
    main_1(inp)

    print "--------------------------------------"
    print "- 2:"
    print "--------------------------------------"
    main_2(inp)
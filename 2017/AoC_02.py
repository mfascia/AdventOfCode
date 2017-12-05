import sys


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(inp):
    cs = 0
    for line in inp:
        values = [int(x) for x in line.split("\t")]
        cs += max(values) - min(values)
    print cs

def main_2(inp):
    cs = 0
    for line in inp:
        values = [int(x) for x in line.split("\t")]
        for i in xrange(0, len(values)):
            for j in xrange(0, len(values)):
                if i == j:
                    continue
                if values[i] == (values[i] / values[j]) * values[j]:
                    cs += values[i] / values[j]

    print cs

if __name__ == "__main__":
    
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
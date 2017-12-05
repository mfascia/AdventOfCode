import sys


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(inp):
    print inp
    pass


def main_2(inp):
    print inp
    pass


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
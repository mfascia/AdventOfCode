import sys
import re


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(inp):
    program = []
    state = {}
    for line in inp:
        match = re.match("([a-z]*) (inc|dec) (-?[0-9]*) if ([a-z]*) (>|<|>=|<=|==|!=) (-?[0-9]*)", line)
        #               0: reg          1: op           2: val               3: reg          4: test         5: val
        program.append([match.group(1), match.group(2), int(match.group(3)), match.group(4), match.group(5), int(match.group(6))])
        state[match.group(1)] = 0
        state[match.group(4)] = 0

    print program
    print state

    tests = {
        "==": (lambda state, reg, val: state[reg] == val),
        "!=": (lambda state, reg, val: state[reg] != val),
        ">=": (lambda state, reg, val: state[reg] >= val),
        "<=": (lambda state, reg, val: state[reg] <= val),
        ">":  (lambda state, reg, val: state[reg] > val),
        "<":  (lambda state, reg, val: state[reg] < val),
    }

    alltime_max = -100000000
    for inst in program:
        if tests[inst[4]](state, inst[3], inst[5]):
            if inst[1] == "inc":
                state[inst[0]] += inst[2]
            else:
                state[inst[0]] -= inst[2]
        curr_max = max(state.values()) 
        alltime_max = max(alltime_max, curr_max)
    
    max_val = max(state.values())
    print max_val, alltime_max

def main_2(inp):
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
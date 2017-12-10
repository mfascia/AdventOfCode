import sys


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main(stream):
    garbage = False
    level = 0
    score = 0
    removed = 0
    i = 0
    while i < len(stream):
        c = stream[i]
        i += 1

        if c == "!":
            i += 1
            print c + ": skip " + stream[i] 
            continue
        
        if garbage:
            if c == ">":
                garbage = False
                print c + ": end garbage" 
                continue
            else:
                print c + ": garbage"                 
                removed += 1
                continue
        else:
            if c == "<":
                garbage = True
                print c + ": start garbage" 
                continue

            elif c == "{":
                level += 1
                score += level
                print c + ": start block " + str(level) + "|" + str(score)  
                continue

            elif c == "}":
                level -= 1
                print c + ": end block" 
                continue

        print c

    print "score = " + str(score)
    print "removed " + str(removed) + " garbage"


if __name__ == "__main__":
    
    inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))
    stream = "".join(inp)

    main(stream)

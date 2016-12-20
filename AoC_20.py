import sys


def read_input(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(text):
    mins = []
    maxs = []
    for line in text:
        interval = [int(x) for x in line.split("-")]
        mins.append(interval[0])
        maxs.append(interval[1])
    
    mins.sort()
    maxs.sort()

    if mins[0] > 0:
        return 0

    i = 0
    j = 0
    s = 0
    while i<len(mins) and j<len(maxs):
        if mins[i] < maxs[j]:
            s += 1
            i += 1
        elif mins[i] > maxs[j]:
            s -= 1
            if s == 0 and mins[i] != maxs[j]+1:
                print "i:", i, "j:",  "1st free:", str(maxs[j]+1)
                break
            j += 1


def main_2(text):
    pass


if __name__ == "__main__":
    text = read_input("AoC_20_input.txt")
    print ("Part 1 ---------------------------------------------------------------------------------------------------------")
    print main_1(text)
    
    print
    
    print ("Part 2 ---------------------------------------------------------------------------------------------------------")
    print main_2(text)


'''

'''
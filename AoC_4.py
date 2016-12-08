import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream
    
def split_name(name):
    split1 = name.rsplit("-", 1)
    letters = split1[0].replace("-", "")
    split1[1] = split1[1].replace("[", " ")
    split1[1] = split1[1].replace("]", "")
    split2 = split1[1].split()
    return split1[0], letters, int(split2[0]), split2[1]

def main(input_stream):
    sum = 0
    real_rooms = []
    for room in input_stream:
        raw_name, name, number, checksum = split_name(room)
        freq = {}
        for char in name:
             freq[char] = freq.get(char, 0) + 1
            
        sorted = []
        for k, v in freq.iteritems():
            sorted.append([k, v])

        sorted.sort(key=lambda x: x[0])
        sorted.sort(key=lambda x: x[1], reverse=1)

        topfreq = ""
        for i in xrange(0, 5):
            topfreq += str(sorted[i][0])

        if topfreq == checksum:
            sum += number
            real_rooms.append([raw_name, number])
    
    print sum

    for room in real_rooms:
        shift = room[1] % 26
        plain = ""
        for c in room[0]:
            if c == "-":
                plain += " "
            else:
                i = ord(c) - ord("a")
                j = (i + shift) % 26
                plain += alphabet[j]
        if "north" in plain:
            print plain, str(room[1])

if __name__ == "__main__":
    input_stream = read_input_stream("AoC_4_input.txt")
    main(input_stream)

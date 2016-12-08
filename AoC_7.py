import sys

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream

def main_1(input_stream):
    count = 0
    for line in input_stream:
        inside_brackets = False
        has_reverse_sequence = False
        for i in xrange(3, len(line)):
            if line[i] == "[":
                inside_brackets = True
            elif line[i] == "]":
                inside_brackets = False
            else:
                if (line[i-3] == line [i]) and (line[i-1] == line[i-2]) and (line[i] != line[i-1]):
                    if inside_brackets:
                        has_reverse_sequence = False
                        break
                    else:
                        has_reverse_sequence = True
        
        if has_reverse_sequence:
            count +=1

    print count

def main_2(input_stream):
    count = 0
    for line in input_stream:
        inside_brackets = False
        in_aba = []
        out_aba = []
        for i in xrange(2, len(line)):
            if line[i] == "[":
                inside_brackets = True
            elif line[i] == "]":
                inside_brackets = False
            else:
                if (line[i-2] == line [i]) and (line[i] != line[i-1]):
                    if inside_brackets:
                        in_aba.append(line[i-2:i+1])
                    else:
                        out_aba.append(line[i-2:i+1])
        
        #if len(in_aba) > 0 or len(out_aba) >0:
        #    print in_aba, out_aba

        for i in out_aba:
            for j in in_aba:
                if i[0] == j[1] and i[1] == j[0]:
                    print in_aba, out_aba
                    count +=1
                    print i, j
                    break

    print count

if __name__ == "__main__":
    input_stream = read_input_stream("AoC_7_input.txt")
    main_1(input_stream)
    print
    main_2(input_stream)


'''
'''
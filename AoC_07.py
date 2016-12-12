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
        
        for i in out_aba:
            found = False
            for j in in_aba:
                if i[0] == j[1] and i[1] == j[0]:
                    count +=1
                    found = True
                    break
            if found:
                break

    print count

if __name__ == "__main__":
    input_stream = read_input_stream("AoC_07_input.txt")
    main_1(input_stream)
    print
    main_2(input_stream)


'''
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba. However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

    abba[mnop]qrst supports TLS (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?

Your puzzle answer was 115.
--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square bracketed sections), and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences. An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba. A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?

Your puzzle answer was 231.
'''
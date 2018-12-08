import sys

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream

def main(input_stream):
    transposed = []
    for i in xrange(0, len(input_stream[0])):
        rot_text = ""
        for j in xrange(0, len(input_stream)):  
            rot_text += input_stream[j][i]
        transposed.append(rot_text)

    for line in transposed:
        freq = {}
        for c in line:
             freq[c] = freq.get(c, 0) + 1

        sorted = []
        for k, v in freq.iteritems():
            sorted.append([k, v])

        sorted.sort(key=lambda x: x[1], reverse=1)
        most_common = sorted[0][0]

        sorted.sort(key=lambda x: x[1], reverse=0)
        least_common = sorted[0][0]

        print most_common, least_common

if __name__ == "__main__":
    input_stream = read_input_stream("2016\\AoC_06_input.txt")
    main(input_stream)


'''
--- Day 6: Signals and Noise ---

Something is jamming your communications with Santa. Fortunately, your signal is only partially jammed, and protocol in situations like this is to switch to a simple repetition code to get the message through.

In this model, the same message is sent repeatedly. You've recorded the repeating message signal (your puzzle input), but the data seems quite corrupted - almost too badly to recover. Almost.

All you need to do is figure out which character is most frequent for each position. For example, suppose you had recorded the following messages:

eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar

The most common character in the first column is e; in the second, a; in the third, s, and so on. Combining these characters returns the error-corrected message, easter.

Given the recording in your puzzle input, what is the error-corrected version of the message being sent?

Your puzzle answer was agmwzecr.
--- Part Two ---

Of course, that would be the message - if you hadn't agreed to use a modified repetition code instead.

In this modified code, the sender instead transmits what looks like random data, but for each character, the character they actually want to send is slightly less likely than the others. Even after signal-jamming noise, you can look at the letter distributions in each column and choose the least common letter to reconstruct the original message.

In the above example, the least common character in the first column is a; in the second, d, and so on. Repeating this process for the remaining characters produces the original message, advent.

Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is trying to send?
'''
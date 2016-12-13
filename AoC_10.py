import sys
import re
import json

solution_part_1 = [17, 61]

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream

def main_1(input_stream):

    value_rules = []
    give_rules = []

    max_bot = -1
    max_out = -1

    for line in input_stream:
        if line[:5] == "value":
            groups = re.match("value ([0-9]*) goes to bot ([0-9]*)", line).groups()
            if len(groups):
                params = [int(t) for t in groups]
                value_rules.append([params[1], params[0]])
                max_bot = max(max_bot, params[1])
        else:
            groups = re.match("bot ([0-9]*) gives low to (bot|output) ([0-9]*) and high to (bot|output) ([0-9]*)", line).groups()
            if len(groups):
                src = int(groups[0])
                low_bot = int(groups[2]) if groups[1] == "bot" else -1
                high_bot = int(groups[4]) if groups[3] == "bot" else -1
                low_out = int(groups[2]) if groups[1] == "output" else -1
                high_out = int(groups[4]) if groups[3] == "output" else -1
                give_rules.append([src, low_bot, high_bot, low_out, high_out])
                max_bot = max(max_bot, low_bot)
                max_bot = max(max_bot, high_bot)
                max_out = max(max_out, low_out)
                max_out = max(max_out, high_out)

    bots = [ [] for x in xrange(0, max_bot+1)]
    outs = [ -1 for x in xrange(0, max_out+1)]

    for vr in value_rules:
        bots[vr[0]].append(vr[1])

    loop = True
    while loop:
        loop = False
        for gr in give_rules:
            if len(bots[gr[0]]) == 2:
                bots[gr[0]].sort()
                if gr[1] != -1: #low bot
                    bots[gr[1]].append(bots[gr[0]][0])
                if gr[2] != -1: # high bot
                    bots[gr[2]].append(bots[gr[0]][1])
                if gr[3] != -1: # low out
                    outs[gr[3]] = bots[gr[0]][0]
                if gr[4] != -1: # high out
                    outs[gr[4]] = bots[gr[0]][1]
                bots[gr[0]] = []
                loop = True

                for i in xrange(0, len(bots)):
                    if bots[i] == [17, 61] or bots[i] == [61, 17]:
                        print "Part 1 solution:", i

    print "Final outputs"
    print outs
    print "Part 2 solution:", str(outs[0]*outs[1]*outs[2])


if __name__ == "__main__":
    input_stream = read_input_stream("AoC_10_input.txt")
    main_1(input_stream)


'''
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does, it gives each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to decide what to do with each chip. You access the local control computer and download the bots' instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

    Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
    Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
    Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
    Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2 contains a value-3 microchip. In this configuration, bot number 2 is responsible for comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?

Your puzzle answer was 73.
--- Part Two ---

What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?

Your puzzle answer was 3965.
'''
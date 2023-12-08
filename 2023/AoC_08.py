import os
import sys
import re
import math
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def parse(text):
	moves = text[0]
	nodes = {}	
	for i in range(2, len(text)):
		node, left, right = re.match("([0-9A-Z]*) = \(([0-9A-Z]*), ([0-9A-Z]*)\)", text[i]).groups()
		nodes[node] = [left, right]

	return moves, nodes
	

def main_1(inp):
	moves, nodes = parse(inp)
	if "AAA" not in nodes.keys():
		return
	
	curr = "AAA"
	m = 0
	steps = 0
	while curr != "ZZZ":
		move = 0 if moves[m] == "L" else 1
		curr = nodes[curr][move]
		m = (m+1) % len(moves)
		steps += 1
	print(steps)


# This works because:
# - Each ghost is on a loop that start at step 0 
# - Each ghost always land the same endpoint and only htat one in its cycle
def main_2(inp):
	moves, nodes = parse(inp)
	ghosts = [x for x in nodes.keys() if x[2] == "A"]
	print(len(ghosts), "ghosts")

	exits = [[] for g in ghosts]

	phases = [-1 for g in ghosts]
	freqs = [-1 for g in ghosts]

	m = 0
	steps = 0
	while True:
		steps += 1
		move = 0 if moves[m] == "L" else 1
		for g in range(len(ghosts)):
			ghosts[g] = nodes[ghosts[g]][move]

			if ghosts[g][2] == "Z":
				if phases[g] == -1:
					phases[g] = steps
				elif freqs[g] == -1:
					freqs[g] = steps - phases[g]

		if -1 not in freqs:
			break
		
		m = (m+1) % len(moves)
	
	print("Phases", phases)
	print("Freqs ", freqs)

	print(math.lcm(*freqs))


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	if doTests:
		# read tests
		if len(tests) == 0:
			i = 0
			while True:
				i += 1
				testfile = sys.argv[0].replace(".py", ("_test_%d.txt" % i))
				if os.path.isfile(testfile):
					tests.append([x for x in read_input(testfile)])
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = [x for x in read_input(sys.argv[0].replace(".py", "_input.txt"))]

	if doTests:
		# run tests
		isTest = True
		print ("--------------------------------------------------------------------------------")
		print ("- TESTS")
		print ("--------------------------------------------------------------------------------")
		for t in range(0, len(tests)):
			if enablePart1:
				print ("--- Test #" + str(t+1) + ".1 ------------------------------")
				main_1(tests[t])
			if enablePart2:
				print ("--- Test #" + str(t+1) + ".2 ------------------------------")
				main_2(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)
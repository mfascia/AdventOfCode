import os
import sys
import re
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def parse(text):
	moves = text[0]
	nodes = {}	
	for i in range(2, len(text)):
		node, left, right = re.match("([A-Z]*) = \(([A-Z]*), ([A-Z]*)\)", text[i]).groups()
		nodes[node] = [left, right]

	print(json.dumps(nodes, indent=4))
	return moves, nodes
	

def main_1(inp):
	moves, nodes = parse(inp)
	curr = "AAA"
	i = 0
	steps = 0
	print(curr)
	while curr != "ZZZ":
		m = 0 if moves[i] == "L" else 1
		curr = nodes[curr][m]
		print(curr)
		i = (i+1) % len(moves)
		steps += 1
	print(steps)


def main_2(inp):
	moves, nodes = parse(inp)
	ghosts = [x for x in nodes.keys() if x[2] == "Z"]

	i = 0
	steps = 0

	while True:
		m = 0 if moves[i] == "L" else 1
		for i in range(len(ghosts)):
			ghosts[i] = nodes[ghosts[i]][m]
			i = (i+1) % len(moves)
			steps += 1
		s = sum([1 for x in ghosts if x[2] == "Z"])
		if s == len(ghosts):
			break
		
	print(steps)



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
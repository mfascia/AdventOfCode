import os
import sys
import re


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

def parseInput(inp):
	lineBreak = 0
	txtStacks = []
	for line in inp:
		lineBreak += 1
		if "1" in line:
			lineBreak += 1
			break
		txtStacks.append(line)

	transposed = ["" for x in txtStacks[0]]
	for y in range(0, len(txtStacks)):
		for x in range(0, len(txtStacks[y])):
			transposed[x] += txtStacks[y][x]

	stacks = [[y for y in x[::-1].strip(" ")] for x in transposed if x[::-1].strip(" ").isalnum()]

	moves = []
	inp = inp[lineBreak:]
	for line in inp:
		m = re.match("move ([0-9]*) from ([0-9]*) to ([0-9]*)", line)
		moves.append([int(x) for x in m.groups()])

	return stacks, moves


def main_1(inp):
	stacks, moves = parseInput(inp)

	for m in moves:
		for i in range(0,m[0]):
			c = stacks[m[1]-1].pop()
			stacks[m[2]-1].append(c)

	top = ""
	for s in stacks:
		top += s[-1]

	print(top)


def main_2(inp):
	stacks, moves = parseInput(inp)

	for m in moves:
		buf = []
		for i in range(0,m[0]):
			c = stacks[m[1]-1].pop()
			buf.append(c)
		stacks[m[2]-1] += buf[::-1]

	top = ""
	for s in stacks:
		top += s[-1]

	print(top)


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip("\n\t"), raw)
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
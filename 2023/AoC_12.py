import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def is_match(springs, groups):
	counts = []
	nb = 0
	acc = False
	for i in range(len(springs)):
		if springs[i] == "#":
			if acc == False:
				acc = True
			if acc:
				nb += 1
		else:
			if acc:
				acc = False
				counts.append(nb)
				nb = 0
	if acc:
		counts.append(nb)
	return groups == counts


def eval_springs(springs, groups, i):
	if i < len(springs):
		if springs[i] == "?":
			try_operational = eval_springs(springs[:i] + "." + springs[i+1:], groups, i+1)
			try_damaged = eval_springs(springs[:i] + "#" + springs[i+1:], groups, i+1)
			return try_operational + try_damaged
		else:
			return eval_springs(springs, groups, i+1)
	else:
		match = is_match(springs, groups) 
		if match:
			print(springs, match)
			return 1
		else:
			return 0
	

def main_1(inp):
	sum = 0
	for line in inp:
		springs, groups = line.split(" ")
		groups = [int(x) for x in groups.split(",")]

		print(springs, groups)
		sum += eval_springs(springs, groups, 0)
		print(sum) 


def main_2(inp):
	sum = 0
	for line in inp:
		springs, groups = line.split(" ")
		springs = springs + "?" + springs + "?" + springs + "?" + springs + "?" + springs
		groups = [int(x) for x in groups.split(",")] * 5

		print(springs, groups)


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
			print()

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
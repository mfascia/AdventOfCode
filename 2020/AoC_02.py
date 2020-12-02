import os
import sys
import re


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	valid = 0

	for line in inp:
		rule, pw = [x.strip() for x in re.split(":", line)]
		freq, letter = [x.strip() for x in re.split(" ", rule)]
		mini, maxi = [int(x.strip()) for x in re.split("-", freq)]

		sum = 0
		for c in pw:
			if c == letter:
				sum += 1

		if mini <= sum and maxi >= sum:
			valid += 1

	print("There are", valid, "valis passwords")


def main_2(inp):
	valid = 0
	
	for line in inp:
		rule, pw = [x.strip() for x in re.split(":", line)]
		pos, letter = [x.strip() for x in re.split(" ", rule)]
		i, j = [int(x.strip())-1 for x in re.split("-", pos)]

		score = 0
		if len(pw) >= i and pw[i] == letter:
			score += 1

		if len(pw) >= j and pw[j] == letter:
			score += 1

		if score == 1:
			valid += 1

	print("There are", valid, "valis passwords")


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
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)
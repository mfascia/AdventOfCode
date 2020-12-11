import os
import sys


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
	adapters = [0] + sorted([int(x) for x in inp])
	rating = max(adapters) + 3
	diffs = [0, 0, 0, 1]
	for i in range(0, len(adapters)-1):
		diffs[adapters[i+1]-adapters[i]] += 1
	print(diffs[1]*diffs[3])

# # Part 2 BRUTE FORCE - works for tests but not input
# #----
# def permutations(adapters, i, res, valid):
# 	if i == len(adapters)-1:
# 		return valid + 1
# 	j = i+1
# 	while j<len(adapters) and adapters[j]-adapters[i] <= 3:
# 		valid = permutations(adapters, j, res + [adapters[i]], valid)
# 		j += 1 
# 	return valid
#
#
# def main_2(inp):
# 	adapters = [0] + sorted([int(x) for x in inp])
# 	rating = max(adapters) + 3
# 	adapters.append(rating)
# 	valid =	permutations(adapters, 0, [], 0)
# 	print("nb of permutations:", valid)
#----


def main_2(inp):
	adapters = [0] + sorted([int(x) for x in inp])
	rating = max(adapters) + 3
	adapters.append(rating)

	# count the number of paths that lead to each element of clusters of adapters with a joltage diff of max 3
	paths = [0 for x in adapters]
	paths[0] = 1
	for i in range(0, len(adapters)):
		for j in range(i+1, len(adapters)):
			if (adapters[j]-adapters[i]) <= 3:
				paths[j] += paths[i]

	print(paths[-1])


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

def foo(a):
	a += 1


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
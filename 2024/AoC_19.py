import os
import sys
from collections import defaultdict


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def match(patterns, design):
	ret = False
	if design == "":
		return True
	for p in patterns:
		if design.startswith(p):
			sub = match(patterns, design[len(p):])
			if sub:
				return True
	return ret


def get_prime_patterns(patterns):
	prime = []
	for i, p in enumerate(patterns):
		sub = patterns[:i] + patterns[i+1:]
		if not match(sub, p):
			prime.append(p)
	# print(patterns)
	# print(prime)
	return prime


def main_1(inp):
	patterns = sorted(inp[0].split(", "))
	designs = inp[2:]
	count = 0

	patterns = get_prime_patterns(patterns)

	for i, d in enumerate(designs):
		if match(patterns, d):
			count += 1
			print(i,"/", len(designs), ": pattern", d, "CAN be made :)")
		else:
			print(i,"/", len(designs), ": pattern", d, "cannot be made :(")
	print(count)


###################################################################################################
# This approach was too slow as there are too many patterns to do a bruteforece recursive approach.
# It worked for part 1 as we identify the subset of prime patterns that are truly unique, which
# considerably shortens the set of patterns to use for the simple recursive approach. 
###################################################################################################
# def match_count(patterns, design, matches = [], pattern = []):
# 	ret = False
# 	if design == "":
# 		matches.append(pattern)
# 		return True
# 	for p in patterns:
# 		if design.startswith(p):
# 			ret = match_count(patterns, design[len(p):], matches, pattern + [p]) or ret
# 	return ret
#
#
# def main_2_slow(inp):
# 	patterns = inp[0].split(", ")
# 	designs = inp[2:]
# 	count = 0
#
# 	patterns = get_prime_patterns(patterns)
#
# 	for i, d in enumerate(designs):
# 		matches = []
# 		if match_count(patterns, d, matches):
# 			count += len(matches)
# 			print(i,"/", len(designs), ": pattern", d, "CAN be made in", len(matches), "ways :)")
# 		else:
# 			print(i,"/", len(designs), ": pattern", d, "cannot be made :(")
# 	print(count)
###################################################################################################


###################################################################################################
# The approach here is to start from the end of the design and work backwards, on character at a time
# We keep track of how many ways we can make the substring on the right of the current position, which
# makes the worst case complexity O( nb_chars_in_design x nb_patterns ), rather than exponential in the
# simple recursive approach from above
###################################################################################################
def main_2(inp):
	patterns = inp[0].split(", ")
	designs = inp[2:]
	count = 0

	for i, d in enumerate(designs):
		mem = defaultdict(lambda:0)
		mem[""] = 1
		for j in range(len(d)-1, -1, -1):
			right = d[j:]
		
			c = 0
			for k, p in enumerate(patterns):
				if right.startswith(p) and mem[right[len(p):]] > 0:
					c += mem[right[len(p):]]
			mem[right] = c
		
		nbways = mem[d]
		count += nbways
		if nbways > 0:
			print(i,"/", len(designs), ": pattern", d, "CAN be made in", nbways, "ways :)")
		else:
			print(i,"/", len(designs), ": pattern", d, "cannot be made :(")
	
	print(count)


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
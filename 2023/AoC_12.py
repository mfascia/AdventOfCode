import os
import sys


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


# We go over the springs from left to right. 
# When we encounter a "?", we will try both options using recursion. 
# As we go, 
# 	we keep track of which group we are in and which spring within that group we are trying to match. 
# 	we stop progressing if the group we are in goes larger than what expected
# 	we ask the cache the following question at the start of each step:
# 		"When we were evaluating the spring at position <pos> while trying to match the spring <spr> of group <grp>, were we successful?"
# 			- if the answer is Yes, then we retun the cached value and stop going any further
#			- if the answer is No, when we come back from the recursion, we score the result in the cache 
#
# Here is an example:
#	.??.# [1, 1]
#
#	.??.# (0, 0, 0) no mem
#	.??.# (1, 0, 0) no mem
#	..?.# (2, 0, 0) no mem					<< trying "." for the first "?"
#		....# (3, 0, 0) no mem				<< trying "." for the second "?"
#		....# (4, 0, 0) no mem
#		....# (5, 0, 1) no mem				<< reached the end of the string, check if it was a match but wasn't
#		-+-+-+-+-+-+-+-+-+-+
#		..#.# (3, 0, 1) no mem				<< trying "#" for the second "?"
#		..#.# (4, 1, 0) no mem
#		..#.# (5, 1, 1) no mem MATCH!!!		<< reached the end of the string, check if it was a match and it was!
#		-+-+-+-+-+-+-+-+-+-+				<< NOTE: as we go up the recursion stack here, we cache that (4, 1, 0) has a count of 1
#	-+-+-+-+-+-+-+-+-+-+					
#	.#?.# (2, 0, 1) no mem					<< trying "#" for the first "?"
#		.#..# (3, 1, 0) no mem				<< trying "." for the second "?"
#		.#..# (4, 1, 0) 1 					<< (4, 1, 0) is in the cache with a count of 1. No need to go further
#		-+-+-+-+-+-+-+-+-+-+
#		.##.# (3, 0, 2) no mem
#		-+-+-+-+-+-+-+-+-+-+
#	-+-+-+-+-+-+-+-+-+-+
#
# --> 2 suitable configurations
def eval_springs(springs, groups, cache={}, pos=0, grp=0, spr=0, depth=""):
	# make sure the cache is clean when we start
	if pos == 0:
		cache.clear()
	
	# cache lookup key
	k = (pos, grp, spr)
	
	if isTest:
		print(depth, springs, k, cache[k] if k in cache else "no mem", "MATCH!!!" if (pos == len(springs) and is_match(springs, groups)) else "")
	
	# if we came across this case, return the cached result
	if k in cache:
		return cache[k]
	
	# if we have a full string, check if we have a match
	if pos == len(springs):
		match = 1 if is_match(springs, groups) else 0
		return match

	count = 0

	# if we don't have a full string yet, progress towards it
	# in case we are at a "?", try both options
	if isTest and springs[pos] == "?":
		depth += "  "
	
	for c in [".", "#"]:
		if springs[pos] == c or springs[pos] == "?":
			if c == ".":
				if spr > 0:
					# starting on next group, ONLY if the one we just finished is of the correct length
					if grp < len(groups) and spr == groups[grp]:
						count += eval_springs(springs[:pos] + c + springs[pos+1:], groups, cache, pos+1, grp+1, 0, depth)
				else:
					# moving up the springs, nothing to see here
					count += eval_springs(springs[:pos] + c + springs[pos+1:], groups, cache, pos+1, grp, spr, depth)
			else:
				# grow current group
				count += eval_springs(springs[:pos] + c + springs[pos+1:], groups, cache, pos+1, grp, spr+1, depth)
		
		if isTest and springs[pos] == "?":
			print(depth, "-+-+-+-+-+-+-+-+-+-+")
	
	cache[k] = count
	return count


def parse_records(text):
	records = []
	for line in text:
		springs, groups = line.split(" ")
		groups = [int(x) for x in groups.split(",")]
		records.append([springs, groups])
	return records

def main_1(inp):
	sum = 0
	records = parse_records(inp)

	for r in records:
		sum += eval_springs(r[0], r[1])
	
	print("Part 1:", sum) 


def main_2(inp):
	sum = 0
	records = parse_records(inp)

	for r in records:
		springs = r[0] + "?" + r[0] + "?" + r[0] + "?" + r[0] + "?" + r[0]
		groups = r[1] * 5

		sum += eval_springs(springs, groups)

	print("Part 2:", sum) 


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
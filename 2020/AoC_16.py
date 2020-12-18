import os
import sys
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = False
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	i = 0
	rules = {}
	while inp[i]:
		cat, rt1 = inp[i].split(": ")
		rt2 = rt1.split(" or ")
		rules[cat] = [[int(y) for y in x.split("-")] for x in rt2]
		i += 1
	
	i += 2
	ticket = [int(x) for x in inp[i].split(",")]
	
	i += 3
	nearby = []
	while i<len(inp):
		nearby.append([int(x) for x in inp[i].split(",")])
		i += 1

	er = 0
	for n in nearby:
		for v in n:
			valid = False
			for c in rules:
				for r in rules[c]:
					if v >= r[0] and v <= r[1]:
						valid = valid or True
						found = True
						break
			if not valid:
				er += v
	
	print("error rate:", er)


def main_2(inp):
	# process input
	i = 0
	rules = {}
	while inp[i]:
		cat, rt1 = inp[i].split(": ")
		rt2 = rt1.split(" or ")
		rules[cat] = { "pos": [], "range": [[int(y) for y in x.split("-")] for x in rt2] }
		i += 1
	
	i += 2
	ticket = [int(x) for x in inp[i].split(",")]
	
	i += 3
	nearby = []
	while i<len(inp):
		nearby.append([int(x) for x in inp[i].split(",")])
		i += 1

	# find invalid tickets
	invalid = []
	for n in range(0, len(nearby)):
		for v in nearby[n]:
			valid = False
			for c in rules:
				for r in rules[c]["range"]:
					if v >= r[0] and v <= r[1]:
						valid = valid or True
						found = True
						break
			if not valid:
				invalid.append(n)
				break

	# remove invalid tickets
	tickets = [nearby[x] for x in range(0, len(nearby)) if x not in invalid]
	tickets.append(ticket)

	# find canidate rules for each column. Multiple rules can fit each column
	for r in rules:
		for i in range(0, len(ticket)):
			found = True
			for n in tickets:
				valid = False
				for k in rules[r]["range"]:
					if n[i] >= k[0] and n[i] <= k[1]:
						valid = True
						break
				if not valid:					
					found = False
					break
			if found:
				rules[r]["pos"].append(i)
	
	# deduce which column is each rule by backtracking from any identified ones
	checksum = 0
	while checksum != len(rules):
		checksum = 0
		for r in rules:
			if len(rules[r]["pos"]) == 1:
				for s in rules:
					if r == s:
						continue
					elif rules[r]["pos"][0] in rules[s]["pos"]: 
						rules[s]["pos"].remove(rules[r]["pos"][0])
			checksum += len(rules[r]["pos"])
	
	# calculate the result by looking up the ticket in the corect locations
	res = 1
	for r in rules:
		if r.startswith("departure"):
			res *= ticket[rules[r]["pos"][0]]
	print(res)


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
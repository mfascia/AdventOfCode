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


def main_1(inp):
	template = inp[0]
	rules = {}
	for line in inp[2:]:
		k, v = line.split(" -> ")
		rules[k] = v

	poly = template
	for loop in range(0, 10):
		expanded = ""
		for i in range(0, len(poly)-1):
			pair = poly[i:i+2]
			expanded += pair[0] + rules[pair]
		expanded += poly[-1]
		poly = expanded

	hist = [0 for x in range(0,26)]
	for p in poly:
		hist[ord(p)-ord("A")] += 1

	histNZ = [x for x in hist if x > 0]
	print(max(histNZ)-min(histNZ))


def main_2(inp):
	template = inp[0]
	rules = {}
	for line in inp[2:]:
		k, v = line.split(" -> ")
		rules[k] = v

	# break the starting pattern into pairs
	pairs = {}
	for i in range(0, len(template)-1):
		pair = template[i:i+2]
		if pair in pairs:
			pairs[pair] += 1
		else:
			pairs[pair] = 1

	# expand each pair into 2 new pairs according to the rules, and do so 40 times
	for loop in range(0, 40):
		expanded = {}
		for k, v in pairs.items():
			p1 = k[0] + rules[k]
			p2 = rules[k] + k[1]
			if p1 not in expanded:
				expanded[p1] = v
			else:
				expanded[p1] += v
			if p2 not in expanded:
				expanded[p2] = v
			else:
				expanded[p2] += v
		pairs = expanded

	# create histogram of letters based on pairs
	hist = [0 for x in range(0, 26)]
	for k, v in pairs.items():
		hist[ord(k[0])-ord("A")] += v
		hist[ord(k[1])-ord("A")] += v
	
	# Remove null entries in histogram and divide by 2 as all the letters will be double counted except from first and last
	hist[ord(template[0])-ord("A")] += 1
	hist[ord(template[-1])-ord("A")] += 1
	histNZ = [int(x/2) for x in hist if x > 0]

	# Round min and max to the nearer integer before calculating final score
	print(max(histNZ)-min(histNZ))



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
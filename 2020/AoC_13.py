import os
import sys
from functools import reduce



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
	earliest = int(inp[0])
	periods = sorted([int(x) for x in inp[1].split(",") if x.isnumeric()])
	shuttle = periods[0]
	wait = earliest
	for p in periods:
		w = p - (earliest % p)
		if w < wait:
			wait = w
			shuttle = p
	print("wait", wait, "and catch shuttle", shuttle)
	print(shuttle * wait)


def findNonCoprimePairs(values):
	coprimes = []
	for i in range(0, len(values)):
		for j in range(i+1, len(values)):
			num = max(values[i], values[j])
			den = min(values[i], values[j])
			if (num % den) == 0:
				coprimes.append([i, j, values[i], values[j]])
	return coprimes


def main_2(inp):
	i = 0
	values = []
	offsets = []
	for v in inp[1].split(","):
		if v.isnumeric():
			values.append(int(v))
			offsets.append(i)
		i += 1

	# verify that the values are coprimes
	cop = findNonCoprimePairs(values)
	if cop:
		print("found pairs that are non coprime:", cop)
		return

	# find a suitable answer for the first value. then increase the step by that value as we will need the 
	# result to be a multiple of the solution of each shuttle 
	step = 1
	t = 1
	i = 0
	while i<len(values):
		t += step
		if (t % values[i]) == (values[i] - offsets[i]) % values[i]:
			step *= values[i]
			i +=1 
	print(t)


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
import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

from collections import deque


def opp(c):
	i = ord(c)
	if i >= 65 and i <= 90:
		return chr(32+i)
	else:
		return chr(i-32)


def react_polymer(polymer):
	poly = polymer
	i = 0
	end = len(poly)-1
	while i < end:
		if poly[i] == opp(poly[i+1]):
			poly = poly[:i] + poly[i+2:]
			i = max(i-1, 0)
			end -= 2
		else:
			i += 1
	return poly


def edit_polymer(polymer, to_be_removed):
	poly = []
	for c in polymer:
		if not c in to_be_removed:
			poly.append(c)
		
	return "".join(poly)


def main_1(inp):
	print len(react_polymer(inp[0]))


def main_2(inp):
	min_length = 10000000
	for i in xrange(0, 26):
		edited = edit_polymer(inp[0], [chr(ord('a')+i), chr(ord('A')+i)])
		length = len(react_polymer(edited))
		min_length = min(min_length, length)
	print "shortest polymer is ", str(min_length)


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
					tests.append(read_input(testfile))
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			print "--- Test #" + str(t) + ".1 ------------------------------"
			main_1(tests[t])
			if enablePart2:
				print "--- Test #" + str(t) + ".2 ------------------------------"
				main_2(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		print "--- Part 1 ------------------------------"
		main_1(inp)
		if enablePart2:
			print "--- Part 1 ------------------------------"
			main_2(inp)
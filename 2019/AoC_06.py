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
enablePart2 = False
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	parents = {}
	nodes = set()
	root = "COM"
	for line in inp:
		a, b = line.split(")")
		nodes.add(a)
		nodes.add(b)
		parents[b] = a
		
	orbits = {}
	total = 0
	for n in nodes:
		orbit = 1
		if parents.has_key(n):
			parent = parents[n]
			while parent != root:
				orbit += 1
				if parents.has_key(parent):
					parent = parents[parent]
			orbits[n] = orbit
			total += orbit

	print root
	print nodes
	print parents
	print orbits
	print total


def main_2(inp):
	pass


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
			if enablePart1:
				print "--- Test #" + str(t+1) + ".1 ------------------------------"
				main_1(tests[t])
			if enablePart2:
				print "--- Test #" + str(t+1) + ".2 ------------------------------"
				main_2(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp)
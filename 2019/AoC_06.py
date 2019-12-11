import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = False
doInput = True
enablePart1 = False
enablePart2 = True
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


def findPath(parents, start, end):
	path = []
	n = start
	while n != end:
		n = parents[n]
		path.append(n)
	return path


def main_2(inp):
	parents = {}
	nodes = set()
	root = "COM"
	for line in inp:
		a, b = line.split(")")
		nodes.add(a)
		nodes.add(b)
		parents[b] = a
		
	orbits = {}
	for n in nodes:
		orbit = 1
		if parents.has_key(n):
			parent = parents[n]
			while parent != root:
				orbit += 1
				if parents.has_key(parent):
					parent = parents[parent]
			orbits[n] = orbit

	path1 = list(reversed(findPath(parents, "YOU", root)))
	path2 = list(reversed(findPath(parents, "SAN", root)))

	print path1, len(path1)
	print path2, len(path2)

	common = 0
	for i in xrange(0, min(len(path1), len(path2))):
		if path1[i] != path2[i]:
			common = i
			break

	print len(path1) + len(path2) - 2 * common


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
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


OFFSET = 1000000


def hashWire(tokens):
	x = 0
	y = 0
	hashes = set()
	for tok in tokens:
		if tok[0] == "U":
			for i in xrange(0, int(tok[1:])):
				y += 1
				hashes.add((x, y))
		elif tok[0] == "D":
			for i in xrange(0, int(tok[1:])):
				y -= 1
				hashes.add((x, y))
		elif tok[0] == "L":
			for i in xrange(0, int(tok[1:])):
				x -= 1
				hashes.add((x, y))
		elif tok[0] == "R":
			for i in xrange(0, int(tok[1:])):
				x += 1
				hashes.add((x, y))
	return hashes


def main_1(inp):
	tokens1 = inp[0].split(",")
	tokens2 = inp[1].split(",")

	hash1 = hashWire(tokens1)
	print "wire 1 has length", len(hash1)
	hash2 = hashWire(tokens2)
	print "wire 2 has length", len(hash2)

	inter = sorted([abs(v[0])+abs(v[1]) for v in hash1 & hash2])
	print inter
	print "Closest intersection is at Manhattan distace of", inter[0]


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
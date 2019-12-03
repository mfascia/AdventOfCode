import os
import sys


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


def runCode(tokens):
	for pc in xrange(0, len(tokens), 4):
		if tokens[pc] == 1:
			tokens[tokens[pc+3]] = tokens[tokens[pc+1]] + tokens[tokens[pc+2]]
		elif tokens[pc] == 2:
			tokens[tokens[pc+3]] = tokens[tokens[pc+1]] * tokens[tokens[pc+2]]
		elif tokens[pc] == 99:
			break


def main_1(inp, doSwaps):
	tokens = [int(x) for x in inp[0].split(",")]
	
	if doSwaps:
		tokens[1] = 12
		tokens[2] = 2

	runCode(tokens)

	print tokens


def main_2(inp):
	tokens = [int(x) for x in inp[0].split(",")]
	
	for x in xrange(0, 99):
		for y in xrange(0, 99):
			t = [i for i in tokens]
			t[1] = x
			t[2] = y

			print "processing ", x, y

			runCode(t)

			if t[0] == 19690720:
				print 100 * x + y
				return


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
				main_1(tests[t], False)
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
			main_1(inp, True)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp)
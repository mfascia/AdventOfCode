import os
import sys
import re


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


def parse_input(text):
	prevs = {}

	for line in text:
		matches = re.match("Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line)
		first = matches.group(1)
		second = matches.group(2)

		if not prevs.has_key(first):
			prevs[first] = [] 
		if not prevs.has_key(second):
			prevs[second] = []
		prevs[second].append(first)
		prevs[second] = [x for x in sorted(prevs[second])]

	return prevs


def main_1(inp):
	prevs = parse_input(inp)

 	seq = ""
	while prevs:
		avails = [x for x in sorted([k for k, v in prevs.items() if len(v) == 0])]
		a = avails[0]
		seq += a
		del(prevs[a])
		for k, v in prevs.items():
			if a in v:
				v.remove(a)
	print seq


def main_2(inp, cost, nb):
	prevs = parse_input(inp)

	t = 0
 	seq = ""
	times = [0 for x in xrange(0, nb)]
	tasks = ["." for x in xrange(0, nb)]

	while prevs or sum(times):
		for e in xrange(0, len(times)):
			if times[e] == 0:
				if tasks[e] != ".":
					for k, v in prevs.items():
						if tasks[e] in v:
							v.remove(tasks[e])
				if prevs:
					avails = [x for x in sorted([k for k, v in prevs.items() if len(v) == 0])]
					if avails:
						a = avails[0]
						tasks[e] = a
						seq += a
						del(prevs[a])
						times[e] += cost + ord(a) - ord("A")
				else:
					tasks[e] = "."
			else:
				times[e] = max(times[e]-1, 0)
		print t, "\t", "\t".join(tasks)
		t += 1
	print seq
	print t


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
				main_2(tests[t], 0, 2)
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
			main_2(inp, 60, 5)
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
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def parse_input(inp):
	pots = inp[0].split(": ")[1]

	rules = {}
	for txt in inp[2:]:
		pattern, state = txt.split(" => ")
		rules[pattern] = state

	return pots, rules


def pad_pots(pots):
	i = pots.index("#")
	padl = "".join(["." for i in xrange(0, 5-pots.index("#"))])
	padr =  "".join(["." for i in xrange(0, 5-"".join([x for x in reversed(pots)]).index("#"))])
	return padl + pots + padr, len(padl)


def main_1(inp, iter):
	pots, rules = parse_input(inp)
	
	start = 0
	for i in xrange(0, iter):
		pots, pad = pad_pots(pots)
		start -= pad
		pots2 = ".."
		for p in xrange(2, len(pots)-2):
			frag = pots[p-2:p+3]
			if rules.has_key(frag):
				pots2 += rules[frag]
			else:
				pots2 += "."
		pots2 += ".."
		pots = pots2

	s = 0
	for i in xrange(0, len(pots)):
		if pots[i] == "#":
			s += i + start
	print s


def main_2(inp, iter):
	pots, rules = parse_input(inp)
	
	start = 0
	scores = []
	for i in xrange(0, 2000):
		pots, pad = pad_pots(pots)
		start -= pad
		pots2 = ".."
		for p in xrange(2, len(pots)-2):
			frag = pots[p-2:p+3]
			if rules.has_key(frag):
				pots2 += rules[frag]
			else:
				pots2 += "."
		pots2 += ".."
		pots = pots2

		s = 0
		for i in xrange(0, len(pots)):
			if pots[i] == "#":
				s += i + start
		scores.append(s)

	delta = scores[-1] - scores[-2]
	print "After 2000 iterations, score is increasing by", delta, "for each iteration"
	print "Therefore for ", iter, "iterations, final score is", scores[-1] + (delta) * (iter-2000)

	
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
				print "--- Test #" + str(t+1) + " ------------------------------"
				main_1(tests[t], 20)
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp, 20)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp, 50000000000)
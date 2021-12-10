import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
#-----------------------------------------------------------------------------------------------

OPENERS = "([{<"
CLOSERS = ")]}>"
SCORES_INVALID = {
	")": 3,
	"]": 57,
	"}": 1197,
	">": 25137
}
SCORES_INCOMPLETE = {
	")": 1,
	"]": 2,
	"}": 3,
	">": 4
}

def main(inp):
	
	invalidScore = 0
	incompleteScores = []

	for line in inp:
		stack = []
		invalid = False
		for c in line:
			if c in CLOSERS:
				if stack[-1] in OPENERS and CLOSERS.index(c) == OPENERS.index(stack[-1]):
					stack.pop()
				else:
					invalidScore += SCORES_INVALID[c]
					print("INVALID:", line, "expected", CLOSERS[OPENERS.index(stack[-1])], "found", c, "score =", invalidScore)
					invalid = True
					break	
			else:
				stack.append(c)
		if not invalid:
			score = 0
			missing = ""
			while len(stack) > 0:
				o = stack.pop()
				c = CLOSERS[OPENERS.index(o)]
				missing += c
				score = score * 5 + SCORES_INCOMPLETE[c]
			incompleteScores.append(score)
			print("INCOMPLETE:", line, "missing", missing, "score =", score, )

	print("invalid score =", invalidScore)

	incompleteScores.sort()
	print("incomplete score =", incompleteScores[int(len(incompleteScores)/2)])


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
			print ("--- Test #" + str(t+1) + ".1 ------------------------------")
			main(tests[t])
		print ()

	if doInput:
		# process input
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		print ("--- Part 1 ------------------------------")
		main(inp)

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


def tokenize(text):
	split = text.split(" ")
	tok = []
	for s in split:
		if s.startswith("("):
			while s[0] == "(":
				tok.append("(")
				s = s[1:]
		if s.endswith(")"):
			p = s.find(")")
			tok.append(s[:p])
			s = s[p:]
			while s and s[0] == ")":
				tok.append(")")
				s = s[1:]
		else:
			tok.append(s)
	return tok


def rpl(toks, prio):
	stack = []
	out = []
	for t in toks:
		if t.isnumeric():
			out.append(int(t))
		elif t in "*+":
			while stack and prio[t] <= prio[stack[-1]]:
				out.append(stack.pop())
			stack.append(t)
		elif t == "(":
			stack.append(t)
		elif t == ")":
			while stack:
				op = stack.pop()
				if op == "(":
					break
				else:
					out.append(op)
	while stack:
		out.append(stack.pop())

	stack = []
	for t in out:
		if t == "+":
			v1 = stack.pop()
			v2 = stack.pop()
			stack.append(v1+v2)
		elif t == "*":
			v1 = stack.pop()
			v2 = stack.pop()
			stack.append(v1*v2)
		else:
			stack.append(t)

	#print(toks, out, stack)

	return stack[0]


def main_1(inp):
	prio = {
		"(": 0,
		"*": 1,
		"+": 1,
	}
	sum = 0
	for line in inp:
		toks = tokenize(line)
		sum += rpl(toks, prio)
	print(sum)


def main_2(inp):
	prio = {
		"(": 0,
		"*": 1,
		"+": 2,
	}
	sum = 0
	for line in inp:
		toks = tokenize(line)
		sum += rpl(toks, prio)
	print(sum)


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
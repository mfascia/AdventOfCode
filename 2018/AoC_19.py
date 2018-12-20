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
verbose = False
#-----------------------------------------------------------------------------------------------


opcodes = [	"addr",	"addi",	"mulr",	"muli",	"banr",	"bani",	"borr",	"bori",	"setr",	"seti",	"gtir",	"gtri",	"gtrr",	"eqir",	"eqri",	"eqrr" ]


def addr(regs, a, b, c):
	regs[c] = regs[a] + regs[b]

def addi(regs, a, b, c):
	regs[c] = regs[a] + b

def mulr(regs, a, b, c):
	regs[c] = regs[a] * regs[b]

def muli(regs, a, b, c):
	regs[c] = regs[a] * b

def banr(regs, a, b, c):
	regs[c] = regs[a] & regs[b]

def bani(regs, a, b, c):
	regs[c] = regs[a] & b

def borr(regs, a, b, c):
	regs[c] = regs[a] | regs[b]

def bori(regs, a, b, c):
	regs[c] = regs[a] | b

def setr(regs, a, b, c):
	regs[c] = regs[a]

def seti(regs, a, b, c):
	regs[c] = a

def gtir(regs, a, b, c):
	regs[c] = 1 if a > regs[b] else 0

def gtri(regs, a, b, c):
	regs[c] = 1 if regs[a] > b else 0

def gtrr(regs, a, b, c):
	regs[c] = 1 if regs[a] > regs[b] else 0

def eqir(regs, a, b, c):
	regs[c] = 1 if a == regs[b] else 0

def eqri(regs, a, b, c):
	regs[c] = 1 if regs[a] == b else 0

def eqrr(regs, a, b, c):
	regs[c] = 1 if regs[a] == regs[b] else 0


def parse_input(inp):
	ipr = -1
	prog = []
	for line in inp:
		tokens = line.split(" ")
		if line[0] == "#":
			ipr = int(tokens[1])
		else:
			instr = [tokens[0]] + [int(x) for x in tokens[1:]]
			prog.append(instr)
	return prog, ipr


def main_1(inp):
	prog, ipr = parse_input(inp)
	print "ip bound to register", ipr

	ip = 0
	regs = [0, 0, 0, 0, 0, 0]

	while ip <len(prog):
		inst = prog[ip]
		regs[ipr] = ip

		if verbose:
			debug = "ip=" + str(ip) + " " + str(regs) + " " + str(inst)

		globals()[inst[0]](regs, inst[1], inst[2], inst[3])

		if verbose:
			debug += " " + str(regs)
			print debug

		ip = regs[ipr] + 1

	print "final registers values:", regs


def main_2(inp):
	# Consider the equation V = W x I for a really large value of V
	# The code is trying to sum all the possible values of W for integer solutions for W and I, starting from W = 1
	# V is computed from some constants that are in the code
	prog, ipr = parse_input(inp)
	
	s = 0

	a = 76 * prog[20][2]
	b = prog[21][2] * 22 + prog[23][2]
	c = 23550 * prog[31][2] * 32
	v = a + b + c
	for i in xrange(1,v+1):
		w = v / i
		if v % i == 0:
			s += w
	print "r0 = ", s 


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
				main_1(tests[t])
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
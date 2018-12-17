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
	examples = []
	prog = []
	before = None
	after = None
	regs = None
	part2 = False
	empty = 0
	for line in inp:
		if not part2:
			if "Before" in line:
				empty = 0
				before = [int(x) for x in line[9:-1].split(", ")]
			elif "After" in line:
				empty = 0
				after = [int(x) for x in line[9:-1].split(", ")]
			elif len(line) == 0:
				if before and regs and after:
					examples.append([before, regs, after])
					before = None
					regs = None
					after = None
				empty += 1
				if empty > 2:
					part2 = True
				continue
			else:
				empty = 0
				regs = [int(x) for x in line.split(" ")]
		else:
			instr = [int(x) for x in line.split(" ")]
			prog.append(instr)
	return examples, prog


def main(inp):
	examples, prog = parse_input(inp)

	stats = {}
	for oc in opcodes:
		stats[oc] = [0 for x in xrange(0, 16)]

	moreThan3 = 0
	for e in examples:
		i = e[1][0]
		nb = 0
		for k,v in stats.items():
			r = [x for x in e[0]]
			globals()[k](r, e[1][1], e[1][2], e[1][3])
			#print k, r, e[2]
			if r == e[2]:
				stats[k][e[1][0]] += 1
				nb += 1
		if nb >= 3:
			moreThan3 += 1

	print moreThan3, "example(s) can map to at least 3 opcodes, out of", len(examples)

	potentialOpcodes = {}
	for k, v in stats.items():
		potentialOpcodes[k] = [x for x in xrange(0,16) if v[x] > 0]
	
	# assuming there is an unambiguous solution and at least one rule is identified  immediately
	# we can remove the identified opcodes from the list of candidates. Rince repeat and it converges
	# to the solution after worst case 16 rounds
	instructionSet = ["" for x in xrange(0,16)]
	for loop in xrange(0, 16):
		for k,v in potentialOpcodes.items():
			if len(v) == 1:
				instructionSet[v[0]] = k
				for a,b in potentialOpcodes.items():
					if v[0] in b:
						potentialOpcodes[a] = [x for x in b if x != v[0]]
	
	print "instruction set:", instructionSet

	regs = [0, 0, 0, 0]
	for p in prog:
		oc = instructionSet[p[0]]
		globals()[oc](regs, p[1], p[2], p[3])
	print "registers after execution of input code:", regs


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
			print "--- Test #" + str(t+1) + " ------------------------------"
			main(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		main(inp)
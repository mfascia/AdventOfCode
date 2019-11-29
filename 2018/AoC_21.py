import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------

'''
#ip 2								ip is in register 2
01		 seti 123 0 4				\\
02		 bani 4 456 4				|| check if 123 AND 456 == 72	0000 0111 1011 AND 0001 0010 1110 =  0000 0100 1000
03		 eqri 4 72 4				//
04		 addr 4 2 2					goto 6 if true, 5 if false
05		 seti 0 0 2					r2 = 0
06		 seti 0 1 4					r4 = 0
07		 bori 4 65536 1				r1 = r4 OR 65536		0000 0001 0000 0000 0000 0000
08		 seti 16031208 7 4			r4 = 16031208			1111 0100 1001 1101 1110 1000
09		 bani 1 255 3				r3 = r1 AND 255 		0000 0000 0000 0000 1111 1111
10		 addr 4 3 4					r4 = r3 + r4
11		 bani 4 16777215 4			r4 = r4 AND 16777215	1111 1111 1111 1111 1111 1111	
12		 muli 4 65899 4				r4 = r4 * 65899			0000 ‭0001 0000 0001 0110 1011‬
13		 bani 4 16777215 4			r4 = r4 AND 16777215	1111 1111 1111 1111 1111 1111
14		 gtir 256 1 3				r3 = r1 <= 256
15		 addr 3 2 2
16		 addi 2 1 2
17		 seti 27 3 2
18		 seti 0 9 3
19		 addi 3 1 5
20		 muli 5 256 5
21		 gtrr 5 1 5
22		 addr 5 2 2
23		 addi 2 1 2
24		 seti 25 7 2
25		 addi 3 1 3
26		 seti 17 4 2
27		 setr 3 1 1
28		 seti 7 5 2
29		 eqrr 4 0 3
30		 addr 3 2 2
31		 seti 5 1 2
'''

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
	pass


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
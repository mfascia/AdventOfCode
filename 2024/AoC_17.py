import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = False
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


class Computer:
	def __init__(self):
		self.pc = 0
		self.a = 0
		self.b = 0
		self.c = 0
		self.mem = []
		self.out = ""

	def __repr__(self):
		return "[pc: {:08d}, a: {:08d} {:032b}, b: {:08d}, c: {:08d}]\t|\t".format(self.pc, self.a, self.a, self.b, self.c) + " ".join([str(x) for x in self.mem]) + "\t\t|\t out: " + self.out

	def combo_op(self, value):
		if value >= 0 and value <= 3:
			return self.mem[self.pc+1]
		if value == 4:
			return self.a
		if value == 5:
			return self.b
		if value == 6:
			return self.c

	def step(self, verbose=False):
		opcodes = str.format("{} {} | ", self.mem[self.pc], self.mem[self.pc+1])
		if verbose:
			dbg = ""
		
		if self.mem[self.pc] == 0:		### adv
			v = (2 ** self.combo_op(self.mem[self.pc+1]))

			if verbose:
				dbg = str.format("adv {} {}", self.a, v)

			self.a = int(self.a / v)
			self.pc += 2

		elif self.mem[self.pc] == 1:	### bxl
			if verbose:
				dbg = str.format("bxl {} {}", self.b, self.mem[self.pc+1])

			self.b = self.b ^ self.mem[self.pc+1]
			self.pc += 2

		elif self.mem[self.pc] == 2:	### bst
			v = self.combo_op(self.mem[self.pc+1]) % 8
			self.b = v
			self.pc += 2

			if verbose:
				dbg = str.format("bst {}", v)

		elif self.mem[self.pc] == 3:	### jnz
			if verbose:
				dbg = str.format("jnz {}", self.mem[self.pc+1] != 0)

			if self.a != 0:
				self.pc = self.mem[self.pc+1]
			else:
				self.pc += 2

		elif self.mem[self.pc] == 4:	### bxc
			if verbose:
				dbg = str.format("bxc {} {}", self.b, self.c)

			self.b = self.b ^ self.c
			self.pc += 2

		elif self.mem[self.pc] == 5:	### out
			v = str(self.combo_op(self.mem[self.pc+1]) % 8)
			if self.out != "":
				self.out += ","
			self.out += str(self.combo_op(self.mem[self.pc+1]) % 8)
			self.pc += 2

			if verbose:
				dbg = str.format("out {}", v)

		elif self.mem[self.pc] == 6:		### bdv
			v = (2 ** self.combo_op(self.mem[self.pc+1]))
			if verbose:
				dbg = str.format("bdv {} {}", self.a, v)

			self.b = int(self.a / v)
			self.pc += 2

		elif self.mem[self.pc] == 7:		### cdv
			v = (2 ** self.combo_op(self.mem[self.pc+1]))
			if verbose:
				dbg = str.format("cdv {} {}", self.a, v)

			self.c = int(self.a / v)
			self.pc += 2
		
		if verbose:
			while len(dbg) < 20:
				dbg += " "
			print(opcodes, dbg, self)

	def run(self, restart=True, verbose=True):
		if restart:
			self.pc = 0
		while self.pc < len(self.mem):
			self.step(verbose)


def main_1(inp):
	c = Computer()
	c.a = int(inp[0][11:]) 	# 2412754513550330
	c.b = int(inp[1][11:])
	c.c = int(inp[2][11:])
	c.mem = [int(x) for x in inp[4][8:].split(",")]
	c.run(True, True)
	print(c.out)


def main_2(inp):
	return
	c = Computer()
	c.a = int(inp[0][11:])
	c.b = int(inp[1][11:])
	c.c = int(inp[2][11:])
	c.mem = [int(x) for x in inp[4][8:].split(",")]

	targets = [2,4,1,2,7,5,4,5,1,3,5,5,0,3,3,0]

	for t in targets:
		a = 64751475
		while len(c.out) == 0 or not "2,4,1,2,7,5,4,5,1,3,5,5,0,3,3,0".startswith(c.out):
			a = a + 1
			print(a, c.out)
			c.pc = 0
			c.a = a
			c.b = 0
			c.c = 0
			c.out = ""
			c.run(False, False)


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
		isTest = True
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
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)
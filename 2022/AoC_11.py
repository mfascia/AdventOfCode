import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


class Monkey:
	def __init__(self, id=0):
		self.id = id
		self.items = []
		self.test = None
		self.if_true = 0
		self.if_false = 0
		self.nb_inspections = 0

	def print(self):
		print("Monkey", self.id, ":", self.items, "inspected", self.nb_inspections)


def read_monkeys(inp):
	monkeys = []
	m = None
	for line in inp:
		if len(line) == 0:
			monkeys.append(m)
		elif "Monkey" in line:
			m = Monkey(id=int(line[7:-1]))
		elif "Starting items:" in line:
			m.items = [int(x) for x in line[16:].split(", ")]
		elif "Operation:" in line:
			op, val = line[21:].split(" ")
			if val == "old":
				if op == "+":
					m.operation = lambda x: x + x
				else:
					m.operation = lambda x: x * x
			else:
				if op == "+":
					m.operation = lambda x, v=int(val): x + v
				else:
					m.operation = lambda x, v=int(val): x * v
		elif "Test: divisible by" in line:
			m.test = int(line[19:])
		elif "If true:" in line:
			m.if_true = int(line[25:])
		elif "If false:" in line:
			m.if_false = int(line[26:])

	monkeys.append(m)
	return monkeys


def do_rounds(monkeys, nbRounds, doBored):

	# calculate a global modulus that can be applied after each round to any numbers to keep the numbers manageably low without messing with the rules
	gm = 1
	for m in monkeys:
		gm *= m.test

	for round in range(0, nbRounds):
		for m in monkeys:
			items = m.items
			m.items = []
			for i in items:
				m.nb_inspections += 1
				i = m.operation(i)
				if doBored:
					i = int(i/3)
				else:
					i = i % gm
				if i % m.test == 0:
					monkeys[m.if_true].items.append(i)
				else:
					monkeys[m.if_false].items.append(i)

		# for m in monkeys:
		# 	m.print()

def main_1(inp):
	monkeys = read_monkeys(inp)
	do_rounds(monkeys, 20, True)

	mostActive = sorted(monkeys,key=lambda x: x.nb_inspections, reverse=True)
	print(mostActive[0].nb_inspections*mostActive[1].nb_inspections)


def main_2(inp):
	monkeys = read_monkeys(inp)
	do_rounds(monkeys, 10000, False)

	mostActive = sorted(monkeys,key=lambda x: x.nb_inspections, reverse=True)
	print(mostActive[0].nb_inspections*mostActive[1].nb_inspections)


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
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


def parse(inp):
	rules = {}
	updates = []
	parseRules = True
	for line in inp:
		if parseRules:
			if line == "":
				parseRules = False
				continue
			else:
				a, b = [int(x) for x in line.split("|")]
				if a in rules:
					rules[a].append(b)
				else:
					rules[a] = [b]
		else:
			updates.append([int(x) for x in line.split(",")])
	return rules, updates


def is_ordered(rules, update):
	ordered = True
	for i in range(len(update)):
		page = update[i]
		sub = [-1]
		if page in rules:
			sub = rules[page]
		for j in range(len(sub)):
			if sub[j] in update[:i]:
				ordered = False
				return False, page, j

	if ordered:
		return True, 0, 0


def main_1(inp):
	rules, updates = parse(inp)
	sum = 0
	for update in updates:
		ordered, page, sub = is_ordered(rules, update)
		if ordered:
			sum += update[int(len(update)/2)]
	print(sum)


def main_2(inp):
	rules, updates = parse(inp)
	sum = 0
	for update in updates:
		fixed = False
		ordered, page, sub = is_ordered(rules, update)
		while not ordered:
			fixed = True
			update.remove(page)
			off = rules[page][sub]
			pos = update.index(off)
			update = update[:pos] + [page] + update[pos:]
			ordered, page, sub = is_ordered(rules, update)
		if fixed:
			sum += update[int(len(update)/2)]
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
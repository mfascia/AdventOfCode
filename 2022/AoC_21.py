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


def build_monkeys_tree(inp):
	monkeys = {}
	for line in inp:
		name, expr = line.split(": ")
		if expr.isalnum():
			monkeys[name] = (lambda v=int(expr): int(v))
		elif "+" in expr:
			left, right = expr.split(" + ")
			monkeys[name] = (lambda a=left, b=right: monkeys[a]() + monkeys[b]())
		elif "-" in expr:
			left, right = expr.split(" - ")
			monkeys[name] = (lambda a=left, b=right: monkeys[a]() - monkeys[b]())
		elif "*" in expr:
			left, right = expr.split(" * ")
			monkeys[name] = (lambda a=left, b=right: monkeys[a]() * monkeys[b]())
		elif "/" in expr:
			left, right = expr.split(" / ")
			monkeys[name] = (lambda a=left, b=right: int(monkeys[a]() / monkeys[b]()))
	return monkeys


def main_1(inp):
	monkeys = build_monkeys_tree(inp)
	print(monkeys["root"]())


def eval_human(monkeys, value):
	monkeys["humn"] = (lambda v=int(value): v)
	return monkeys["root"]()


def main_2(inp):
	monkeys = build_monkeys_tree(inp)
	for line in inp:
		if "root" in line:
			name, expr = line.split(": ")
			left, op, right = expr.split(" ") 
			monkeys[name] = (lambda a=left, b=right: monkeys[a]() - monkeys[b]())
			break

	# binary searching the human value within a very large interval	
	# lower end
	imin = -100000000000000
	rmin = eval_human(monkeys, imin)

	imax = 1000000000000000
	rmax = eval_human(monkeys, imax)
	
	while True:
		mid = int((imax + imin)/2)
		r = eval_human(monkeys, mid)
		print("humn:", mid, "--> root:", r)
		if r == 0:
			break
		elif min(rmin, r) < 0 and max(rmin, r) > 0:
			imax = mid
			rmax = r
		elif min(rmax, r) < 0 and max(rmax, r) > 0:
			imin = mid
			rmin = r


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
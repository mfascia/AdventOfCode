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

def eval(target, lhs, rhs, concat):
	if len(rhs) == 0:
		return lhs == target
	elif len(rhs) == 1:
		if concat and int(str(lhs) + str(rhs[0])) == target:
			return True
		elif lhs + rhs[0] == target:
			return True
		elif lhs * rhs[0] == target:
			return True
		else:
			return False
	else:
		v = rhs[0]
		rhs = rhs[1:]
		if concat and eval(target, int(str(lhs) + str(v)), rhs, concat):
			return True
		elif eval(target, lhs + v, rhs, concat):
			return True
		else:
			return eval(target, lhs * v, rhs, concat)


def main_1(inp):
	sum = 0
	for line in inp:
		result, rhs = line.split(": ")
		result = int(result)
		args = [int(x) for x in rhs.split(" ")]

		if eval( result, args[0], args[1:], False):
			sum += result

	print(sum)



def main_2(inp):
	sum = 0
	for line in inp:
		result, rhs = line.split(": ")
		result = int(result)
		args = [int(x) for x in rhs.split(" ")]

		if eval( result, args[0], args[1:], True):
			sum += result

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
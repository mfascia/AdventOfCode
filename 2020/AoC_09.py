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


def findInvalid(val, pre):
	j = pre
	for j in range(pre, len(val)):
		i = j-pre
		v = val[j]
		valid = False
		for m in range(i, j):	 
			for n in range(m+1, j): 
				if val[m] + val[n] == v:
					valid = True
					break
			if valid:
				break
		if not valid:
			return v


def main_1(inp, pre):
	val = [int(x) for x in inp]
	invalid = findInvalid(val, pre)
	print("invalid:", invalid)


def main_2(inp, pre):
	val = [int(x) for x in inp]
	invalid = findInvalid(val, pre)

	for i in range(0, len(val)):
		acc = val[i]
		for j in range(i+1, len(val)):
			acc += val[j]
			if acc == invalid:
				weak = min(val[i:j+1]) + max(val[i:j+1])
				print("weakness:", weak)
				return
			elif acc > invalid:
				break


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
				main_1(tests[t], 5)
			if enablePart2:
				print ("--- Test #" + str(t+1) + ".2 ------------------------------")
				main_2(tests[t], 5)
			print ()

	if doInput:
		# process input
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp, 25)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp, 25)
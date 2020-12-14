import os
import sys
import re


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


def main_1(inp):
	mask = ""
	mem = {}
	for line in inp:
		lhs, rhs = line.split(" = ")
		if lhs == "mask":
			mask = rhs
		else:
			matches = re.findall("[0-9]+", lhs)
			addr = int(matches[0])
			val =  "{0:036b}".format(int(rhs))
			masked = ""
			for i in range(0, len(mask)):
				if mask[i] == "X":
					masked = masked + val[i]
				else:
					masked = masked + mask[i]
			mem[addr] = int(masked, 2)

	acc = 0
	for a in mem:
		acc += mem[a]
	print(acc)


def genFloatingAdresses(mask):
	i = mask.find("X") 
	if i >= 0:
		return genFloatingAdresses(mask[:i] + "0" + mask[i+1:]) + genFloatingAdresses(mask[:i] + "1" + mask[i+1:])
	else:
		return [mask]


def main_2(inp):
	mask = ""
	mem = {}
	for line in inp:
		lhs, rhs = line.split(" = ")
		if lhs == "mask":
			mask = rhs
		else:
			matches = re.findall("[0-9]+", lhs)
			val =  int(rhs)
			addr = "{0:036b}".format(int(matches[0]))
			masked = ""
			for i in range(0, len(mask)):
				if mask[i] == "0":
					masked = masked + addr[i]
				elif mask[i] == "1":
					masked = masked + "1"
				else:
					masked = masked + "X"
			writeto = []
			if "X" in masked:
				writeto = genFloatingAdresses(masked)
			else:
				writeto.append(masked)

			for a in writeto:
				mem[int(a, 2)] = val
	
	acc = 0
	for a in mem:
		acc += mem[a]
	print(acc)


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
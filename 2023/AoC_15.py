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
enablePart2 = False
#-----------------------------------------------------------------------------------------------


def parse_commands(text):
	valves = text[0].split(",")
	return valves


def hash_command(command):
	hash = 0
	for char in command:
		hash = ((hash + ord(char)) * 17) % 256 
	return hash


def decode_command(cmd):
	pos = cmd.index("=")
	if pos > -1:
		label = cmd[:pos]
		hash = hash_command(label)
		op = cmd[pos]
		value = int(cmd[pos+1:])
	else:
		pos = cmd.index()
		label = cmd[:pos]
		hash = hash_command(label)
		op = cmd[pos]
	
	return label, hash, op, value


def main_1(inp):
	commands = parse_commands(inp)
	total = sum(map(lambda x: hash_command(x), commands))
	print(total)


def main_2(inp):
	commands = parse_commands(inp)
	total = 0
	boxes = [[] for x in range(256)]
	for cmd in commands:
		label, hash, op, value = decode_command(cmd)


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
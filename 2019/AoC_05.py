import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def fetchParam(tokens, pc, mode):
	param = 0
	if mode == 1:
		param = tokens[pc]
	else:
		param = tokens[tokens[pc]]
	return param


def runCode(tokens, inputStream):
	pc = 0
	outputStream = []
	i = 0
	while pc<len(tokens):
		op = int(str(tokens[pc])[-2:])
		modes = [int(v) for v in list(reversed(str(tokens[pc])[:-2]))]
		while len(modes) < 3:
			modes.append(0)

		# ADD 
		if op == 1:
			p1 = fetchParam( tokens, pc+1, modes[0])
			p2 = fetchParam( tokens, pc+2, modes[1])
			tokens[tokens[pc+3]] = p1 + p2
			pc += 4

		# MUL
		elif op == 2:
			p1 = fetchParam( tokens, pc+1, modes[0])
			p2 = fetchParam( tokens, pc+2, modes[1])
			tokens[tokens[pc+3]] = p1 * p2
			pc += 4

		# INPUT
		elif op == 3:
			tokens[tokens[pc+1]] = inputStream[i]
			pc += 2

		# OUTPUT
		elif op == 4:
			p1 = fetchParam( tokens, pc+1, modes[0])
			outputStream.append(p1)
			pc += 2

		# JUMP IF TRUE
		elif op == 5:
			p1 = fetchParam( tokens, pc+1, modes[0])
			p2 = fetchParam( tokens, pc+2, modes[1])
			if p1 != 0:
				pc = p2
			else:
				pc += 3

		# JUMP IF FALSE
		elif op == 6:
			p1 = fetchParam( tokens, pc+1, modes[0])
			p2 = fetchParam( tokens, pc+2, modes[1])
			if p1 == 0:
				pc = p2
			else:
				pc += 3

		# LESS THAN
		elif op == 7:
			p1 = fetchParam( tokens, pc+1, modes[0])
			p2 = fetchParam( tokens, pc+2, modes[1])
			if p1 < p2:
				tokens[tokens[pc+3]] = 1
			else:
				tokens[tokens[pc+3]] = 0
			pc += 4

		# EQUALS
		elif op == 8:
			p1 = fetchParam( tokens, pc+1, modes[0])
			p2 = fetchParam( tokens, pc+2, modes[1])
			if p1 == p2:
				tokens[tokens[pc+3]] = 1
			else:
				tokens[tokens[pc+3]] = 0
			pc += 4

		# END
		elif tokens[pc] == 99: 
			break

	return outputStream


def main_1(inp, inputStream):
	tokens = [int(x) for x in inp[0].split(",")]
	
	outputStream = runCode(tokens, inputStream)

	print outputStream


def main_2(inp, inputStream):
	tokens = [int(x) for x in inp[0].split(",")]
	
	outputStream = runCode(tokens, inputStream)

	print outputStream


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	if doInput:
		inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp, [1])
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp, [5])
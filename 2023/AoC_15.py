import os
import sys
import json


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


def parse_commands(text):
	valves = text[0].split(",")
	return valves


def hash_command(command):
	hash = 0
	for char in command:
		hash = ((hash + ord(char)) * 17) % 256 
	return hash


def decode_command(cmd):
	if "=" in cmd:
		pos = cmd.index("=")
		label = cmd[:pos]
		hash = hash_command(label)
		op = cmd[pos]
		value = int(cmd[pos+1:])
		return label, hash, op, value
	else:
		pos = cmd.index("-")
		label = cmd[:pos]
		hash = hash_command(label)
		op = cmd[pos]
		return label, hash, op, 0


def print_boxes(boxes):
	for i, b in boxes.items():
		# if len(b[0]) == 0:
		#  	continue 
		txt = "Box " + str(i) + ": "
		for j in range(len(b[0])):
			txt += "[" + b[0][j] + " " + str(b[1][j]) + "] "
		print(txt)
	print()


def main_1(inp):
	commands = parse_commands(inp)
	total = sum(map(lambda x: hash_command(x), commands))
	print(total)


def main_2(inp):
	commands = parse_commands(inp)
	boxes = {}
	for cmd in commands:
		label, hash, op, value = decode_command(cmd)
		if not hash in boxes:
			boxes[hash] = [[], []]
		match op:
			case "=":
				if label in boxes[hash][0]:
					pos = boxes[hash][0].index(label)
					boxes[hash][1][pos] = value
				else:
					boxes[hash][0].append(label)
					boxes[hash][1].append(value)
			case "-":
				if label in boxes[hash][0]:
					pos = boxes[hash][0].index(label)
					boxes[hash][0] = boxes[hash][0][:pos] + boxes[hash][0][pos+1:]
					boxes[hash][1] = boxes[hash][1][:pos] + boxes[hash][1][pos+1:]
		if isTest:
			print("After \"", cmd, "\"")
			print_boxes(boxes)


	power = 0
	for i, b in boxes.items():
		for j in range(len(b[1])):
			p = (i+1) * (j+1) * b[1][j]
			power += p

	print(power)


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
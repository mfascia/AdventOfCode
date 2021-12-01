import os
import sys
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def eval(text, pos, rules, r):
	rule = rules[r]
	
	if rule["type"] == "char":
		if text[pos] == rule["char"]:
			return True, 1
		else: 
			return False, 0

	elif rule["type"] == "seq":
		res = True
		oldpos = pos
		i = 0
		while res and i<len(rules[r]["seq"]) and pos<len(text):
			res, consumed = eval(text, pos, rules, rules[r]["seq"][i])
			if not res:
				return False, 0
			else:
				i += 1
				pos += consumed
		return True, pos-oldpos
	
	elif rule["type"] == "or":
		if r == 8 or r == 11:
			pipo = 1
		res = True
		i = 0
		oldpos = pos
		while res and i<len(rules[r]["lhs"]) and pos<len(text):
			res, consumed = eval(text, pos, rules, rules[r]["lhs"][i])
			if not res:
				break
			else:
				i += 1
				pos += consumed
		if res:
			return res, pos-oldpos
		else:
			res = True
			i = 0
			pos = oldpos
			while res and i<len(rules[r]["rhs"]) and pos<len(text):
				res, consumed = eval(text, pos, rules, rules[r]["rhs"][i])
				if not res:
					return False, 0
				else:
					i += 1
					pos += consumed
			return True, pos-oldpos


def main_1(inp): 
	rules = {}

	i = 0
	line = inp[i]
	while line:
		nb, rule = line.split(": ")
		if rule.startswith("\""):
			rules[int(nb)] = {
				"type": "char",
				"char": rule[1]
			}
		elif " | " in rule:
			parts = rule.split(" | ")
			rules[int(nb)] = {
				"type": "or",
				"lhs": [int(x) for x in parts[0].split(" ")],
				"rhs": [int(x) for x in parts[1].split(" ")]
			}
		else:
			rules[int(nb)] = {
				"type": "seq",
				"seq": [int(x) for x in rule.split(" ")]
			}
		i += 1
		line = inp[i]

	count = 0
	for j in range(i+1, len(inp)):
		line = inp[j]
		res = eval(line, 0, rules, 0)
		if res[0] and res[1] == len(line):
			print(line, "matches rule 0")
			count += 1
		else:
			print(line, "DOES NOT matches rule 0")
	print(count, "strings match rule 0")


def main_2(inp):
	rules = {}

	i = 0
	line = inp[i]
	while line:
		nb, rule = line.split(": ")
		if rule.startswith("\""):
			rules[int(nb)] = {
				"type": "char",
				"char": rule[1]
			}
		elif " | " in rule:
			parts = rule.split(" | ")
			rules[int(nb)] = {
				"type": "or",
				"lhs": [int(x) for x in parts[0].split(" ")],
				"rhs": [int(x) for x in parts[1].split(" ")]
			}
		else:
			rules[int(nb)] = {
				"type": "seq",
				"seq": [int(x) for x in rule.split(" ")]
			}
		i += 1
		line = inp[i]

	rules[8] = {
		"type": "or",
		"rhs": [42],
		"lhs": [42, 8]
	}

	rules[11] = {
		"type": "or",
		"rhs": [42, 31],
		"lhs": [42, 11, 31]
	}

	count = 0
	for j in range(i+1, len(inp)):
		line = inp[j]
		res = eval(line, 0, rules, 0)
		if res[0] and res[1] == len(line) == 0:
			print(line, "matches rule 0")
			count += 1
		else:
			print(line, "DOES NOT matches rule 0")
	print(count, "strings match rule 0")


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
import os
import sys
import re
import json


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

def parseRules(inp):
	rules = {}
	for line in inp:
		left, right = line.split(" bags contain ")
		rules[left] = {}
		if right != "no other bags.":
			for c in right.split(", "):
				tok = c.split(" ")
				rules[left][tok[1] + " " + tok[2]] = int(tok[0])
	#print(json.dumps(rules, indent=2))
	return rules


def containsShinyGoldBag(rules, bag):
	result = False
	for c in rules[bag]:
		if c == "shiny gold":
			result = True
		else:
			result = result or containsShinyGoldBag(rules, c)
	return result


def main_1(inp):
	rules = parseRules(inp)

	result = 0
	for color in rules:
		if color == "shiny gold":
			continue
		found = containsShinyGoldBag(rules, color)
		if found:
			result += 1
	print(result)


def nbInnerBags(rules, bag):
	nb = 0
	for c in rules[bag]:
		nb += rules[bag][c] * (1 + nbInnerBags(rules, c))
	return nb


def main_2(inp):
	rules = parseRules(inp)
	nb = nbInnerBags(rules, "shiny gold")
	print(nb)



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
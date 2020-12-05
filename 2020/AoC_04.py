import os
import sys
from functools import reduce


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
	passport = {}
	valid = 0
	for line in inp:
		if len(line) == 0:
			if len(passport) == 8 or (len(passport) == 7 and "cid" not in passport):
				valid += 1
			passport = {}
		else:
			tokens = line.split(" ")
			for tok in tokens:
				key, value = tok.split(":")
				passport[key] = value
		
	if len(passport) == 8 or (len(passport) == 7 and "cid" not in passport):
		valid += 1

	print( "Found", valid, "valid passport(s).")


def main_2(inp):
	passport = {}
	potentially_valid = []
	for line in inp:
		if len(line) == 0:
			if len(passport) == 8 or (len(passport) == 7 and "cid" not in passport):
				potentially_valid.append(passport)
			passport = {}
		else:
			tokens = line.split(" ")
			for tok in tokens:
				key, value = tok.split(":")
				passport[key] = value
		
	if len(passport) == 8 or (len(passport) == 7 and "cid" not in passport):
		potentially_valid.append(passport)

	valid = 0
	for p in potentially_valid:
		score = 0
		if int(p["byr"]) >= 1920 and int(p["byr"]) <= 2002:
			score += 1
		if int(p["iyr"]) >= 2010 and int(p["iyr"]) <= 2020:
			score += 1
		if int(p["eyr"]) >= 2020 and int(p["eyr"]) <= 2030:
			score += 1
		if (p["hgt"].endswith("cm") and int(p["hgt"][:-2]) >= 150 and int(p["hgt"][:-2]) <= 193) or (p["hgt"].endswith("in") and int(p["hgt"][:-2]) >= 59 and int(p["hgt"][:-2]) <= 76):
			score += 1
		if p["hcl"][0] == "#" and len(p["hcl"]) == 7 and reduce(lambda x, y: x and y, map(lambda x: x in "0123456789abcdef", p["hcl"][1:])):
			score += 1
		if p["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
			score += 1
		if len(p["pid"]) == 9 and reduce(lambda x, y: x and y, map(lambda x: x in "0123456789", p["pid"])):
			score += 1
		
		if score == 7:
			valid += 1
		else:
			valid = valid

	print( "Found", valid, "valid passport(s).")


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
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


def main_1(inp):
	sum = 0
	for line in inp:
		num = ""
		for c in line:
			if c in "0123456789":
				num += c
		if len(num) > 0:
			num = num[0] + num[-1]
			sum += int(num)
	print(sum)


DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
STIGID = [x[::-1] for x in DIGITS]

def find_left_digit(text):
	for i in range(len(text)):
		if text[i] in "0123456789":
			return text[i]
		for d in DIGITS:
			if text[i:min(len(text),i+len(d))] == d:
				return str(DIGITS.index(d))
	return ""

def find_right_digit(text):
	text = text[::-1]
	for i in range(len(text)):
		if text[i] in "0123456789":
			return text[i]
		for d in STIGID:
			if text[i:min(len(text),i+len(d))] == d:
				return str(STIGID.index(d))
	return ""

def main_2(inp):
	sum = 0
	for line in inp:
		code = find_left_digit(line) + find_right_digit(line)
		sum += int(code)
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
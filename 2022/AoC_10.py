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

SAMPLES = [20, 60, 100, 140, 180, 220]


def execute_program(inp):
	c = 1
	x = 1
	hist = [[c, x ]]
	for line in inp:
		c = c+1
		hist.append([c, x])
		if line != "noop":
			c = c+1
			x += int(line[5:])
			hist.append([c, x])
	return hist


def main_1(inp):
	hist = execute_program(inp)

	v = 0
	for s in SAMPLES:
		if s<len(hist):
			print(hist[s-1])
			v += hist[s-1][0] * hist[s-1][1]
	print(v)


def main_2(inp):
	hist = execute_program(inp)

	p = 0
	i = 0
	txt = ""
	for y in range(0, 6):
		txt = ""
		for x in range(0, 40):
			p = 40*y + x
			if p < len(hist) and x >= hist[p][1]-1 and x <= hist[p][1]+1:
				txt += "#"
			else:
				txt += "."
		print(txt)


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
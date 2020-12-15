import os
import sys
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [
	"10, 0, 3, 6",
	"2020, 0, 3, 6",
	"2020, 1, 3, 2",
	"2020, 2, 1, 3",
	"2020, 1, 2, 3",
	"2020, 2, 3, 1",
	"2020, 3, 2, 1",
	"2020, 3, 1, 2"
	]
inp = "2020, 1, 0, 16, 5, 17, 4"

doTests = False
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	ages = [int(x) for x in inp.split(",")]
	lut = {0:[]}
	i = 0
	for a in ages[1:]:
		i += 1
		lut[a] = [i]

	turns = ages[0]
	for t in range(len(ages), turns+1):
		last = ages[t-1]
		if last in lut and len(lut[last]) > 1:
			d = lut[last][-1] - lut[last][-2]
			ages.append(d)
			if d in lut:
				lut[d].append(t)
			else:
				lut[d] = [t]
		elif last in lut:
			ages.append(0)
			lut[0].append(t)
		else:
			ages.append(0)
			lut[0] = [t]
	
	print(ages[-1])


def main_2(inp):
	print("Be patient, this will take 30s to 1 minute...")
	main_1(inp.replace("2020", "30000000"))


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
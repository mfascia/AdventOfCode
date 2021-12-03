import os
import sys


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


def main_1(inp):
	one = [0 for x in inp[0]]
	zer = [0 for x in inp[0]]
	for line in inp:
		for i in range(0, len(line)):
			if line[i] == "1":
				one[i] += 1
			else:
				zer[i] += 1
	print(one)
	print(zer)
	gamma = ""
	epsilon = ""
	for i in range(0, len(one)):
		if one[i] > zer[i]:
			gamma += "1"
			epsilon += "0"
		else:
			gamma += "0"
			epsilon += "1"
	g = int(gamma, base=2)
	e = int(epsilon, base=2)
	print( gamma, g)
	print( epsilon, e)
	print( g*e)	


def main_2(inp):
	oxy = [x for x in inp]
	for b in range(0, len(oxy[0])):
		bitcount = 0
		bitcount = sum([int(x[b]) for x in oxy])
		if bitcount >= len(oxy)/2:
			oxy = list(filter( lambda x: x[b] == "1", oxy))
		else:
			oxy = list(filter( lambda x: x[b] == "0", oxy))
		if len(oxy) == 1: 
			break
	oxy_val = int(oxy[0], 2)
	print("oxy", oxy_val)
 
	co2 = [x for x in inp]
	for b in range(0, len(co2[0])):
		bitcount = 0
		bitcount = sum([int(x[b]) for x in co2])
		if bitcount < len(co2)/2:
			co2 = list(filter( lambda x: x[b] == "1", co2))
		else:
			co2 = list(filter( lambda x: x[b] == "0", co2))
		if len(co2) == 1: 
			break
	co2_val = int(co2[0], 2)
	print("co2", co2_val)
	print( oxy_val * co2_val)


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
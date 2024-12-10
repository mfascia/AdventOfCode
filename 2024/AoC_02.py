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


def assess(levels):
	diffs = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
	safe = True
	if diffs[0] == 0:
		return False
	elif diffs[0] > 0:	# ascending
		for d in diffs:
			if d < 1 or d > 3:
				safe = False
				continue
	else: # descending
		for d in diffs:
			if d > -1 or d <-3:
				safe = False
				continue
	return safe


def main_1(inp):
	count = 0
	for line in inp:
		levels = [int(x) for x in line.split(" ")]
		safe = assess(levels)
		if safe:
			count += 1
	print(count)


def main_2(inp):
	count = 0
	for line in inp:
		levels = [int(x) for x in line.split(" ")]
		safe = assess(levels)
		if safe:
			count += 1
		else:
			for skip in range(len(levels)):
				patched = levels[:skip] + levels[skip+1:]
				safe = assess(patched)
				if safe:				
					count += 1
					break
	print(count)

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
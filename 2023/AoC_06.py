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


def parse_values(line):
	header, values = line.split(":")
	values = values.strip(" ")
	compact = ""
	while compact != values:
		compact = values.replace("  ", " ")
		values, compact = compact, values
	data = [int(x) for x in values.split(" ")]
	return data


def dist(time, held):
	if held >= time:
		return 0
	else:
		return (time - held) * held


def main_1(inp):
	races = []

	times = parse_values(inp[0])
	dists = parse_values(inp[1])

	product = 1
	for i in range(len(times)):
		time = times[i]
		toBeat = dists[i]
		waysToWin = 0
		for t in range(time):
			if dist(time, t) > toBeat:
				waysToWin += 1
		product *= waysToWin

	print("Part 1:", product)


def main_2(inp):
	time = int(inp[0][5:].replace(" ",""))
	record = int(inp[1][9:].replace(" ",""))
	print(time, record)

	# binary search what press time starts beating the record
	t = int(time/2)
	dt = int(time/4)
	while dt >= 1:
		dmax = dist(time, t)
		if dmax > record:
			t = t - dt
		else:
			t = t + dt
		if dt == 1 and record < dmax:
			break
		else:
			dt = int(dt / 2 + 0.5)

	# the ime that stops beating the record is symmetrical (see picture and spreadsheet)
	print("Part 2:", time - 2*t - 1)


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
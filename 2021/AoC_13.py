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
#-----------------------------------------------------------------------------------------------


def main(inp):
	doingDots = True
	dots = []
	folds = []
	for line in inp:
		if len(line) == 0:
			doingDots = False
			continue

		if doingDots:
			dots.append([int(x) for x in line.split(",")])
		else:
			a, b = line.split("=")
			folds.append([a[-1], int(b)])

	foldsCount = 0
	for f in folds:
		if f[0] == "x":
			for i in range(0, len(dots)):
				if dots[i][0] > f[1]:
					dots[i][0] = 2*f[1] - dots[i][0]
		else:
			for i in range(0, len(dots)):
				if dots[i][1] > f[1]:
					dots[i][1] = 2*f[1] - dots[i][1]
		foldsCount += 1
		if foldsCount == 1:
			uniqueDots = []
			for d in dots:
				if d not in uniqueDots:
					uniqueDots.append(d)
			print("Unique dots after step", foldsCount, "=", len(uniqueDots))

	maxX = max([x[0] for x in dots])
	maxY = max([x[1] for x in dots])
	grid = [[" " for x in range(0, maxX+1)] for y in range(0, maxY+1)]
	for d in dots:
		grid[d[1]][d[0]] = "#"
	for r in grid:
		print("".join(r))


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
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)
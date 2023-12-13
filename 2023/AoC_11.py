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


def empty_space(text):
	empty_x = []
	empty_y = []
	x = 0
	for x in range(len(text[0])):
		empty = True
		for y in range(len(text)):
			if text[y][x] == "#":
				empty = False
				break
		if empty:
			empty_x.append(x)

	for y in range(len(text)):
		if not "#" in text[y]:
			empty_y.append(y)

	return empty_x, empty_y


def list_galaxies(text):
	galaxies = []
	for y in range(len(text)):
		for x in range(len(text[0])):
			if text[y][x] == "#":
				galaxies.append([x, y])
	return galaxies


def manatthan(a, b, empty_x, empty_y, e):
	xmin = min(a[0], b[0])
	xmax = max(a[0], b[0])
	ymin = min(a[1], b[1])
	ymax = max(a[1], b[1])
	dist = xmax - xmin + ymax - ymin
	for x in range(xmin, xmax+1):
		if x in empty_x:
			dist += e-1
	for y in range(ymin, ymax+1):
		if y in empty_y:
			dist += e-1
	return dist 


def main(inp):
	empty_x, empty_y = empty_space(inp)

	galaxies = list_galaxies(inp)
	dist = 0
	
	for i in range(len(galaxies)-1):
		for j in range(i+1, len(galaxies)):
			dist += manatthan(galaxies[i], galaxies[j], empty_x, empty_y, 2)
	print("Part 1:", dist)

	dist = 0
	for i in range(len(galaxies)-1):
		for j in range(i+1, len(galaxies)):
			dist += manatthan(galaxies[i], galaxies[j], empty_x, empty_y, 1000000)
	print("Part 2:", dist)


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
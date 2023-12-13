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

def compare_line(grid, a, b, tolerance=0):
	aaa = grid[a]
	bbb = grid[b]
	zipped =  zip(aaa, bbb)
	mapped = map(lambda x: x[0] != x[1], zipped)
	summed = sum(mapped)
	return summed <= tolerance

def compare_column(grid, a, b, tolerance=0):
	aaa = [line[a] for line in grid]
	bbb = [line[b] for line in grid]
	return sum(map(lambda x: x[0] != x[1], zip(aaa, bbb))) <= tolerance


def check_horizontal_symmetry_at_row(grid, y, tolerance=0):
	z = y+1
	while y >= 0 and z<len(grid):
		if not compare_line(grid, y, z, tolerance):
			return False
		y -= 1
		z += 1
	return True


def check_vertical_symmetry_at_column(grid, x, tolerance=0):
	z = x+1
	while x >= 0 and z<len(grid[0]):
		if not compare_column(grid, x, z, tolerance):
			return False
		x -= 1
		z += 1
	return True


def check_symmetries(grid, tolerance=0):
	w = len(grid[0])
	h = len(grid)
	hs = []
	vs = [] 
	for y in range(0, h-1):
		if check_horizontal_symmetry_at_row(grid, y, tolerance):
			hs.append(y+1)
	for x in range(0, w-1):
		if check_vertical_symmetry_at_column(grid, x, tolerance):
			vs.append(x+1)
	return hs, vs


def main_1(inp):
	grids = []
	grid = []
	for line in inp:
		if line == "" and len(grid) > 0:
			grids.append(grid)
			grid = []
		else:
			grid.append(line)
	grids.append(grid)

	sh = []
	sv = []
	for g in grids:
		h, v = check_symmetries(g, 0)
		sh += h
		sv += v
	print(sum(sv) + 100*sum(sh))


def main_2(inp):
	grids = []
	grid = []
	for line in inp:
		if line == "" and len(grid) > 0:
			grids.append(grid)
			grid = []
		else:
			grid.append(line)
	grids.append(grid)

	sh = []
	sv = []
	for g in grids:
		h, v = check_symmetries(g, 1)
		sh += h
		sv += v
		h, v = check_symmetries(g, 0)
		for s in h:
			sh.remove(s)
		for s in v:
			sv.remove(s)
	print(sum(sv) + 100*sum(sh))


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
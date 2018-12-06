import os
import sys


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


def parse_input(text):
	points = []
	for line in text:
		x, y = line.split(", ")
		points.append([int(x), int(y)])
	return points


def main_1(inp, size, offset):
	grid = [ [-1 for x in xrange(0, size)] for y in xrange(0, size)]
	points = parse_input(inp)
	for j in xrange(0, size):
		y = j - offset
		for i in xrange(0, size):
			x = i - offset
			mdists = []
			for p in xrange(0, len(points)):
				mdists.append(abs(points[p][0]-x) + abs(points[p][1]-y))
			min_md = min(mdists)
			nearest = mdists.index(min_md)
			grid[j][i] = -1 if mdists.count(min_md) > 1 else nearest

	# scan edges of grid to collect points with infinite influence	
	inf_points = []
	for i in xrange(0, size):
		p = grid[0][i]
		if not p in inf_points:
			inf_points.append(p)
		p = grid[size-1][i]
		if not p in inf_points:
			inf_points.append(p)
		p = grid[i][0]
		if not p in inf_points:
			inf_points.append(p)
		p = grid[i][size-1]
		if not p in inf_points:
			inf_points.append(p)

	valid_points = [p for p in xrange(0, len(points)) if p not in inf_points]
	areas = [0 for x in xrange(0, len(points))]
	for j in xrange(0, size):
		for i in xrange(0, size):
			if grid[j][i] == -1:
				continue		
			if grid[j][i] not in valid_points:
				continue
			areas[grid[j][i]] += 1

	print "point", areas.index(max(areas)), "has max area with", max(areas)


def main_2(inp, size, offset, range):
	grid = [ [0 for x in xrange(0, size)] for y in xrange(0, size)]
	points = parse_input(inp)
	safeArea = 0
	for j in xrange(0, size):
		y = j - offset
		for i in xrange(0, size):
			x = i - offset
			for p in xrange(0, len(points)):
				grid[j][i] += abs(points[p][0]-x) + abs(points[p][1]-y)
			if grid[j][i] < range:
				safeArea += 1
	print safeArea


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
					tests.append(read_input(testfile))
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			if enablePart1:
				print "--- Test #" + str(t) + ".1 ------------------------------"
				main_1(tests[t], 10, 0)
			if enablePart2:
				print "--- Test #" + str(t) + ".2 ------------------------------"
				main_2(tests[t], 10, 0, 32)
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp, 400, 50)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp, 1000, 500, 10000)
import os
import sys
from collections import defaultdict


from AoC import Vector, ADJ_4


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


def print_grid(grid, bounds, start=None, end=None, path=None):
	for y in range(bounds[1].y):
		txt = ""
		for x in range(bounds[1].x):
			p = Vector(x, y)
			if path and p in path:
				txt += "O"
			elif start and p == start:
				txt += "S"
			elif end and p == end:
				txt += "E"
			else:
				txt += grid[y][x]
		print(txt)


def parse_grid(inp):
	grid = []
	bounds = [Vector(), Vector(len(inp[0]), len(inp))]
	for y, line in enumerate(inp):
		row = []
		for x, c in enumerate(line):
			if c == "S":
				start = Vector(x, y)
				row.append(".")
			elif c == "E":
				end = Vector(x, y)
				row.append(".")
			else:
				row.append(c)
		grid.append(row)
	return grid, bounds, start, end


def find_track(grid, bounds, start, end):
	track = {}
	pos = start
	while pos != end:
		track[pos] = len(track)
		for npos in pos.neighbours(ADJ_4, *bounds):
			if grid[npos.y][npos.x] == "." and not npos in track.keys():
				pos = npos
	track[pos] = len(track)
	return track


def expand(points, exclude=[]):
	expanded = []
	for p in points:
		for np in p.neighbours(ADJ_4):
			if not np in expanded and not np in points and not np in exclude:
				expanded.append(np)
	return expanded


def find_cheats(grid, bounds, path):
	cheats = defaultdict(lambda:[])
	for y in range(1, bounds[1].y-1):
		for x in range(1, bounds[1].x-1):
			p = Vector(x, y)
			if grid[y][x] == "#":
				n4 = p.neighbours(ADJ_4)
				if grid[n4[0].y][n4[0].x] == "." and grid[n4[1].y][n4[1].x] == ".":
					i = path[n4[0]]
					j = path[n4[1]]
					cheats[abs(j-i)-2].append(p)
				elif grid[n4[2].y][n4[2].x] == "." and grid[n4[3].y][n4[3].x] == ".":
					i = path[n4[2]]
					j = path[n4[3]]
					cheats[abs(j-i)-2].append(p)
	return cheats


def main_1(inp):
	grid, bounds, start, end = parse_grid(inp)
	track = find_track(grid, bounds, start, end)
	if isTest:
		print_grid(grid, bounds, start, end, track)
	cheats = find_cheats(grid, bounds, track)
	count = 0
	for k, v in cheats.items():
		if k >= 100:
			count += len(v)
	print(count, "save at least 100 picoseconds.")


def main_2(inp):
	pass


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
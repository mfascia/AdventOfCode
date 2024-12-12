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


class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)
	
	def __str__(self):
		return "({0},{1})".format(self.x, self.y)

	def __invert__(self):
		return Vector(-self.x, -self.y)

	def clip(self, bmin, bmax):
		clipped = False
		if self.x < bmin.x:
			self.x = bmin.x
			clipped = True
		if self.x >= bmax.x:
			self.x = bmax.x-1
			clipped = True
		if self.y < bmin.y:
			self.y = bmin.y
			clipped = True
		if self.y >= bmax.y:
			self.y = bmax.y-1
			clipped = True
		return clipped
	
	def from_list(list):
		return Vector(list[0], list[1])


NDIRS = {
	"^": ">",
	">": "v",
	"v": "<",
	"<": "^",
}

MOVES = {
	"^": Vector( 0, -1),
	"v": Vector( 0, 1),
	"<": Vector(-1,  0),
	">": Vector( 1,  0),
}


def parse(inp):
	grid = []
	
	found = False
	y = 0
	for line in inp:
		if not found:
			for c in NDIRS.keys():
				if c in line:
					x = line.index(c)
					if x > 0:
						guard = Vector(x, y)
						found = True
		grid.append([x for x in line])
		y += 1
	
	bounds = [Vector(0, 0), Vector(len(grid[0]), len(grid))]
	return grid, bounds, guard


def step(grid, bounds, guard):
	nloc = False	# True if land on unvisited location
	blocked = True
	dir = grid[guard.y][guard.x]
	while blocked:
		npos = guard + MOVES[dir]
		if npos.clip(*bounds):
			return False, False, npos, True
		elif grid[npos.y][npos.x] == "#":
			dir = NDIRS[dir]
		else:
			if grid[npos.y][npos.x] == ".":
				nloc = True
			if grid[npos.y][npos.x] == dir:
				return True, True, npos, False
			guard = npos
			grid[guard.y][guard.x] = dir
			blocked = False

	## print the grid at each step for debug
	# for row in grid:
	# 	print("".join(row))
	# print()

	return True, False, guard, nloc


def main_1(inp):
	grid, bounds, guard = parse(inp)
	
	count = 0
	inside = True
	loop = False
	while inside and not loop:
		inside, loop, guard, nloc = step(grid, bounds, guard)
		if nloc:
			count += 1
		elif loop:
			print("Guard is stuck in a loop! Exiting...")
	
	for row in grid:
		print("".join(row))
	print()
	print(count)


def main_2(inp):
	grid, bounds, guard = parse(inp)

	count = 0
	for y in range(bounds[1].y):
		for x in range(bounds[1].x):
			grid, bounds, guard = parse(inp)
			if grid[y][x] == ".":
				grid[y][x] = "#"
				inside = True
				loop = False
				while inside and not loop:
					inside, loop, guard, nloc = step(grid, bounds, guard)
				if loop:
					count += 1
					grid[y][x] = "O"
					for row in grid:
						print("".join(row))
					print()
				grid[y][x] = "."
	
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
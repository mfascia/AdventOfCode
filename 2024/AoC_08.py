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


def antinode(bounds, a, b, harmonics):
	dx = b.x - a.x
	dy = b.y - a.y
	ans = []
	p = Vector(a.x-dx, a.y-dy)
	while not p.clip(*bounds):
		ans.append(p)
		if not harmonics:
			break
		p = Vector(p.x-dx, p.y-dy)

	p = Vector(b.x+dx, b.y+dy)
	while not p.clip(*bounds):
		ans.append(p)
		if not harmonics:
			break
		p = Vector(p.x+dx, p.y+dy)
	return ans


def parse(inp):
	antennas = {}
	grid = []
	bounds = [Vector(0, 0), Vector(len(inp[0]), len(inp))]
	for y in range(bounds[1].y):
		row = []
		for x in range(bounds[1].x):
			c = inp[y][x]
			if c.isalnum():
				if c in antennas.keys():
					antennas[c].append(Vector(x, y))
				else:
					antennas[c] = [Vector(x, y)]
			row.append(c)
		grid.append(row)
	return grid, bounds, antennas


def main_1(inp):
	count = 0
	grid, bounds, antennas = parse(inp)
	for k, v in antennas.items():
		if len(v) > 1:
			for i in range(0, len(v)-1):
				for j in range(i+1, len(v)):
					ans = antinode(bounds, v[i], v[j], False)
					for an in ans:
						if grid[an.y][an.x] != "#":
							count += 1
						grid[an.y][an.x] = "#"

	for row in grid:
		print("".join(row))
	print() 

	print("# unique antinodes:", count)


def main_2(inp):
	grid, bounds, antennas = parse(inp)
	for k, v in antennas.items():
		if len(v) > 1:
			for i in range(0, len(v)-1):
				grid[v[i].y][v[i].x] = "#"
				for j in range(i+1, len(v)):
					grid[v[j].y][v[j].x] = "#"
					ans = antinode(bounds, v[i], v[j], True)
					for an in ans:
						grid[an.y][an.x] = "#"

	count = 0
	for y in range(bounds[1].y):
		for x in range(bounds[1].x):
			if grid[y][x] == "#":
				count += 1

	for row in grid:
		print("".join(row))
	print() 

	print("# unique antinodes:", count)


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
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


DIRS = {
	"U": Vector( 0, -1),
	"D": Vector( 0, 1),
	"L": Vector(-1,  0),
	"R": Vector( 1,  0),
}

def main_1(inp):

	bbmin = Vector()
	bbmax = Vector()

	count = 0

	# Extract bounds
	digger = Vector(0, 0)
	for line in inp:
		dir, length, color = line.split(" ")
	
		for i in range(int(length)):
			v = Vector(digger.x + DIRS[dir].x, digger.y + DIRS[dir].y)
			digger = v
			bbmin.x = min(bbmin.x, v.x)
			bbmin.y = min(bbmin.y, v.y)
			bbmax.x = max(bbmax.x, v.x)
			bbmax.y = max(bbmax.y, v.y)

	bbmax.x += 1
	bbmax.y += 1
	
	# Create grid
	grid = [ ["." for x in range(bbmin.x, bbmax.x)] for y in range(bbmin.y, bbmax.y)]

	# Dig Edges
	digger = Vector(0, 0)
	for line in inp:
		dir, length, color = line.split(" ")
		color = color[2:-1]
		for i in range(int(length)):
			v = Vector(digger.x + DIRS[dir].x, digger.y + DIRS[dir].y)
			digger = v
			grid[digger.y-bbmin.y][digger.x-bbmin.x] = "#"
			count += 1

	# Flood fill
	start = Vector(1-bbmin.x, 1-bbmin.y)
	toCheck = [start]

	while toCheck:
		v = toCheck.pop()
		if grid[v.y][v.x] == ".":
			grid[v.y][v.x] = "O"
			count += 1
			for d in DIRS.values():
				nv = v + d
				if not nv.clip(Vector(0, 0), bbmax-bbmin):
					toCheck.append(nv)

	# y = 0
	# for row in grid:
	# 	print(y , "".join(row))
	# 	y += 1
	print(count)


def main_2(inp):
	corners = []
	v = Vector()
	corners.append(v)
	for line in inp:
		_, _, color = line.split(" ")
		dir = "RDLU"[int(color[7])]
		length = int("0x" + color[2:-2], 16)
		nv = Vector(v.x + DIRS[dir].x*length, v.y + DIRS[dir].y*length)
		v = nv
		corners.append(v)

	a = 0
	p = 0
	for c in range(len(corners)-1):
		c1 = corners[c]
		c2 = corners[c+1]
		det = c1.x*c2.y - c1.y*c2.x
		a += det
		p += abs(c2.x - c1.x) + abs(c2.y - c1.y)

	print(int(a/2)+int(p/2)+1)


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
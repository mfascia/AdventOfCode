import os
import sys
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
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
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __repr__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
	
	def __hash__(self):
		return hash(self.x) + hash(self.y)

	# Clips against bmin (inclusive) and bmax (exclusive)
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

	# Tests against bmin (inclusive) and bmax (exclusive)
	def is_inside(self, bmin, bmax):
		return self.x >= bmin.x and self.x < bmax.x and self.y >= bmin.y and self.y < bmax.y

	def from_list(list):
		return Vector(list[0], list[1])

	def neighbours(self, points, bmin=None, bmax=None):
		neigh = []
		for a in points:
			n = self+a
			if bmin and bmax:
				if self.clip(bmin, bmax):
					neigh.append(n)
			else:
				neigh.append(n)
		return neigh


ADJ_4 = [Vector(0, 1), Vector(0, -1), Vector(1, 0), Vector(-1, 0)]
ADJ_DIAGS = [Vector(1, 1), Vector(1, -1), Vector(-1, 1), Vector(-1, -1)]
ADJ_8 = ADJ_4 + ADJ_DIAGS


def parse(inp):
	bounds = [Vector(0, 0), Vector(len(inp[0]), len(inp))]
	return inp, bounds


class Region:
	def __init__(self):
		self.type = 0
		self.perimeter = 0
		self.area = 0
		self.price1 = 0
		self.price2 = 0
		self.cells = []
		self.corners = []

	def __repr__(self):
		if isTest:
			return "type: " + self.type \
				+ "\n.  area: " + str(self.area) \
					+ "\n.  perimeter: " + str(self.perimeter) \
						+ "\n.  price1: " + str(self.price1) \
							+ "\n.  price2: " + str(self.price2) \
								+ "\n.  cells: (" + str(len(self.cells)) + ") " + "".join([x.__repr__() for x in self.cells]) \
									 + "\n.  corners: (" + str(len(self.corners)) + ") " + "".join([x.__repr__() for x in self.corners])
		else:
			return "type: " + self.type \
				+ "\n.  area: " + str(self.area) \
					+ "\n.  perimeter: " + str(self.perimeter) \
						+ "\n.  price1: " + str(self.price1) \
							+ "\n.  price2: " + str(self.price2) \
								+ "\n.  #cells: " + str(len(self.cells)) \
									+ "\n.  #corners: " + str(len(self.corners))
	


CORNER_TAPS = [
	[Vector(-1, -1), Vector(-1, 0), Vector(0, -1)],
	[Vector(1, -1), Vector(1, 0), Vector(0, -1)],
	[Vector(-1, 1), Vector(-1, 0), Vector(0, 1)],
	[Vector(1, 1), Vector(1, 0), Vector(0, 1)]
]

def find_region(grid, bounds, seed):
	reg = Region()
	visited = set()
	reg.type = grid[seed.y][seed.x]
	unseen = [seed]
	while len(unseen) > 0:
		p = unseen.pop()
		if not p.is_inside(*bounds) or grid[p.y][p.x] != reg.type: 
			reg.perimeter += 1
		elif not p in visited:
			if p.is_inside(*bounds) and grid[p.y][p.x] == reg.type:
				reg.area += 1
				reg.cells.append(p)
				unseen += p.neighbours(ADJ_4)
			else:
				reg.perimeter += 1
			visited.add(p)

	reg.price1 = reg.perimeter * reg.area
	
	# Corner detection:
	# ----------------
	# We consider these 4 configurations for a cell (A) and its 4 diagonal neighbours (D) with their 2 adjacent cells (x) 
	#
	#       Bx.          .xD          ...         ...
	#       xA.          .Ax          xA.         .Ax
	#       ...          ...          Dx.         .xD 
	#
	# A cell is a corner if:
	#	- D is differnt from A and the 2 x cells are of the same type
	# 	- A and D are of the same type but the x cells are different type than A and D
	#
	# We do that for each configuration so a cell can report itself as a corner up to 4 times
	for c in reg.cells:
		for ct in CORNER_TAPS:
			count = 0
			nei = c.neighbours(ct)
			if not nei[0].is_inside(*bounds) or grid[nei[0].y][nei[0].x] != reg.type:
				for n in nei:
					if not n.is_inside(*bounds) or grid[n.y][n.x] != reg.type:
						count += 1
				if count == 1 or count == 3:
					reg.corners.append(c)
			elif nei[0].is_inside(*bounds) and (grid[nei[0].y][nei[0].x] == reg.type) and (grid[nei[1].y][nei[1].x] != reg.type) and (grid[nei[2].y][nei[2].x] != reg.type):
				reg.corners.append(c)

	reg.price2 = len(reg.corners) * reg.area
	return reg
 

def main(inp):
	grid, bounds = parse(inp)
	regions = []
	visited = set()
	for y in range(bounds[1].y):
		for x in range(bounds[1].x):
			p = Vector(x, y)
			if not p in visited:
				r = find_region(grid, bounds, p)
				for c in r.cells:
					visited.add(c)
				regions.append(r)
	
	price1 = 0
	price2 = 0
	for r in regions:
		price1 += r.price1
		price2 += r.price2
	print("total price 1:", price1)
	print("total price 2:", price2)


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
import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
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
		if self.x >= bmin.x:
			self.x = bmin.x-1
			clipped = True
		if self.y < bmin.y:
			self.y = bmin.y
			clipped = True
		if self.y >= bmin.y:
			self.y = bmin.y-1
			clipped = True
		return clipped
	
	def from_list(list):
		return Vector(list[0], list[1])


def main_1(inp):
	a = Vector(1, 2)
	b = 3*a
	print(a, b)
	print(b-a)
	c = Vector.from_list([5, 6])
	print(c)
	pass


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
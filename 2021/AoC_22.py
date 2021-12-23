import os
import sys
import re
import time


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

X = 0
Y = 1
Z = 2

class Box:
	def __init__(self, x1, x2, y1, y2, z1, z2):
		self.min = (min(x1, x2), min(y1, y2), min(z1, z2))
		self.max = (max(x1, x2), max(y1, y2), max(z1, z2))

	def __str__(self):
		return f"[{self.min} --> {self.max}]"

	def volume(self):
		return (self.max[0]-self.min[0]) * (self.max[1]-self.min[1]) * (self.max[2]-self.min[2])

	def split(self, v, axis):
		if self.min[axis] < v and v < self.max[axis]:
			if axis == X:
				a = Box(self.min[0], v, self.min[1], self.max[1], self.min[2], self.max[2])
				b = Box(v, self.max[0], self.min[1], self.max[1], self.min[2], self.max[2])
			elif axis == Y:
				a = Box(self.min[0], self.max[0], self.min[1], v, self.min[2], self.max[2])
				b = Box(self.min[0], self.max[0], v, self.max[1], self.min[2], self.max[2])
			elif axis == Z:
				a = Box(self.min[0], self.max[0], self.min[1], self.max[1], self.min[2], v)
				b = Box(self.min[0], self.max[0], self.min[1], self.max[1], v, self.max[2])
			return [a, b]
		else:
			return [self]


	def cut_by(self, other):
		boxes = [self]
		for a in range(0,3):
			sub = []
			for b in boxes:
				sub += b.split(other.min[a], a)
			boxes = sub
			sub = []
			for b in boxes:
				sub += b.split(other.max[a], a)
			boxes = sub
		return tuple(boxes)

	def contains(self, other):
		return self.min[X] <= other.min[X] and self.max[X] >= other.max[X] and self.min[Y] <= other.min[Y] and self.max[Y] >= other.max[Y] and self.min[Z] <= other.min[Z] and self.max[Z] >= other.max[Z]



	def tests():
		a = Box(0, 10, 0, 10, 0, 10)
		b = Box(5, 15, 5, 15, 5, 15)
		c = Box(3, 3, 3, 7, 7, 7)
		print(a)
		print(b)

		pieces = b.cut_by(a)
		for p in pieces:
			print(p)
 
		print(a.contains(b))
		print(a.contains(c))
		print(a.contains(a))
		print(c.contains(a))


def main(inp, init):
	start_time = time.time()
	if init:
		bounds = Box(-50, 51, -50, 51, -50, 51)
	boxes = []
	lineCount = 0
	for line in inp:
		lineCount += 1
		match = re.match("(on|off) x=([-,0-9]*)\.\.([-,0-9]*),y=([-,0-9]*)\.\.([-,0-9]*),z=([-,0-9]*)\.\.([-,0-9]*)", line)
		groups = match.groups()
		if groups:
			box = Box(int(groups[1]), int(groups[2])+1, int(groups[3]), int(groups[4])+1, int(groups[5]), int(groups[6])+1)
			if init and not bounds.contains(box):
				print("Out of bouds: ", line, "SKIPPED")
				continue
			if len(boxes) == 0 and groups[0] == "on":
				boxes.append(box)
			else:
				newBoxes = []
				for b in boxes:
					if not box.contains(b):
						splits = b.cut_by(box)
						if len(splits) > 1:
							for s in splits:
								if not box.contains(s):
									newBoxes.append(s)
						else:
							newBoxes.append(b)
				if groups[0] == "on":
					newBoxes.append(box)
				boxes = newBoxes
			print(lineCount, "/", len(inp), "# boxes:", len(boxes), "(%.8s s)" % (time.time() - start_time))
		else:
			print("could not parse:", line)

	volume = 0
	for b in boxes:
		volume += b.volume()
	print(lineCount, "/", len(inp), "# boxes:", len(boxes), ", volume:", volume, "(%.8s s)" % (time.time() - start_time))


def main_1(inp):
	main(inp, True)


def main_2(inp):
	main(inp, False)


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
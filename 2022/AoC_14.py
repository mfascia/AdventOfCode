import os
import sys
from PIL import Image


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

SAND_COLOR = (220, 178, 128)
TL = 0
BR = 1
DIM = 1000


class Cave:
	def read(self, inp):
		self.rock = []
		self.bbox = [[10000, 10000], [-1, -1]]
		for line in inp:
			points = [[int(y) for y in x.split(",")] for x in line.split(" -> ")]
			
			for i in range(len(points)-1):
				a = points[i]
				b = points[i+1]
				if a[0] == b[0]:
					self.bbox[TL][1] = min(self.bbox[TL][1], min(a[1], b[1]))
					self.bbox[BR][1] = max(self.bbox[BR][1], max(a[1], b[1]))
					for y in range(min(a[1], b[1]), max(a[1], b[1])+1):
						self.rock.append([a[0], y])
				else:
					self.bbox[TL][0] = min(self.bbox[TL][0], min(a[0], b[0]))
					self.bbox[BR][0] = max(self.bbox[BR][0], max(a[0], b[0]))
					for x in range(min(a[0], b[0]), max(a[0], b[0])+1):
						self.rock.append([x, a[1]])

		self.spawner = [500, 0]
		self.bbox[TL][0] = min(self.bbox[TL][0], self.spawner[0])
		self.bbox[TL][1] = min(self.bbox[TL][1], self.spawner[1])
		self.bbox[BR][0] = max(self.bbox[BR][0], self.spawner[0])
		self.bbox[BR][1] = max(self.bbox[BR][1], self.spawner[1])
		
		self.sand = []
		

	def save_image(self, suffix=""):
		bb = [[x for x in self.bbox[TL]], [x for x in self.bbox[BR]]]
		for s in self.sand:
			bb[TL][0] = min(bb[TL][0], s[0])
			bb[TL][1] = min(bb[TL][1], s[1])
			bb[BR][0] = max(bb[BR][0], s[0])
			bb[BR][1] = max(bb[BR][1], s[1])
		bb[TL][0] -= 10
		bb[TL][1] -= 10
		bb[BR][0] += 10
		bb[BR][1] += 10
		sx = bb[1][0] - bb[0][0]
		sy = bb[1][1] - bb[0][1]

		im = Image.new(mode="RGB", size=(sx, sy))	
		for y in range(sy):
			for x in range(sx):
				pt = [x+bb[TL][0], y+bb[TL][1]]
				if pt in self.rock:
					im.putpixel((x, y), (255, 255, 255))
				elif pt in self.sand:
					im.putpixel((x, y), SAND_COLOR)

		im.putpixel((self.spawner[0]-bb[TL][0], self.spawner[1]-bb[TL][1]), (255, 0, 0))

		filename = sys.argv[0][:-3]
		if isTest:
			filename += "-test-" + suffix + ".png"
		else:
			filename += "-input-" + suffix + ".png"

		im.save(filename)


	def simulate_part1(self):
		self.sand = []

		lut = [[0 for x in range(DIM)] for y in range(DIM)]
		for r in self.rock:
			lut[r[1]][r[0]] = 1 		
			
		moreSand = True
		while moreSand:
			moreSand = False
			p = self.spawner
			while p[1] < self.bbox[BR][1] and lut[p[1]][p[0]] != 2:
				q = [p[0], p[1]+1]
				if lut[q[1]][q[0]] == 0:
					p = q
				else:
					q = [p[0]-1, p[1]+1]
					if lut[q[1]][q[0]] == 0:
						p = q
					else:
						q = [p[0]+1, p[1]+1]
						if lut[q[1]][q[0]] == 0:
							p = q
						else:
							self.sand.append(p)
							lut[p[1]][p[0]] = 2
							moreSand = True
							break


	def simulate_part2(self):
		self.sand = []

		lut = [[0 for x in range(DIM)] for y in range(DIM)]
		for r in self.rock:
			lut[r[1]][r[0]] = 1 		
		for x in range(DIM):
			lut[self.bbox[BR][1] + 2][x] = 3
		
		moreSand = True
		while moreSand:
			moreSand = False
			p = self.spawner
			while lut[p[1]][p[0]] != 2:
				q = [p[0], p[1]+1]
				if lut[q[1]][q[0]] == 0:
					p = q
				else:
					q = [p[0]-1, p[1]+1]
					if lut[q[1]][q[0]] == 0:
						p = q
					else:
						q = [p[0]+1, p[1]+1]
						if lut[q[1]][q[0]] == 0:
							p = q
						else:
							self.sand.append(p)
							lut[p[1]][p[0]] = 2
							moreSand = True
							break


def main_1(inp):
	cave = Cave()
	cave.read(inp)
	#cave.save_image("initial-part1")
	cave.simulate_part1()
	#cave.save_image("final-part1")
	print(len(cave.sand))


def main_2(inp):
	cave = Cave()
	cave.read(inp)
	#cave.save_image("initial-part2")
	cave.simulate_part2()
	#cave.save_image("final-part2")
	print(len(cave.sand))
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


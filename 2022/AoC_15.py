import os
import sys
import re


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

class AABB:
	def __init__(self):
		self.xmin = 0
		self.xmax = 0
		self.ymin = 0
		self.ymax = 0

	def __str__(self):
		return "min: " + str(self.min_point()) + ", max: " + str(self.max_point())

	def min_point(self):
		return [self.xmin, self.ymin]

	def max_point(self):
		return [self.xmax, self.ymax]

	def add_point(self, pt):
		self.xmin = min(self.xmin, pt[0])
		self.xmax = max(self.xmax, pt[0])
		self.ymin = min(self.ymin, pt[1])
		self.ymax = max(self.ymax, pt[1])

	def add_point(self, x, y):
		self.xmin = min(self.xmin, x)
		self.xmax = max(self.xmax, x)
		self.ymin = min(self.ymin, y)
		self.ymax = max(self.ymax, y)


class Sensor:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0
		self.dist = 0
	
	def __str__(self):
		return "x=" + str(self.x) + ", y=" + str(self.y) + ", dx=" + str(self.dx) + ", dy=" + str(self.dy) + ", dist=" + str(self.dist)

	def get_closest_outside_points(self):
		outside = self.dist+1
		points = []
		for y in range(self.y-outside, self.y+outside+1):
			dx = outside - (abs(self.y - y))
			points.append([self.x-dx, y])
			if dx > 0:
				points.append([self.x+dx, y])
		return points


def main_1(inp):	
	sensors = []
	aabb = AABB()
	for line in inp:
		values = [int(x) for x in re.match("Sensor at x=(\-?[0-9]*), y=(\-?[0-9]*): closest beacon is at x=(\-?[0-9]*), y=(\-?[0-9]*)", line).groups()]
		s = Sensor()
		s.x = values[0]
		s.y = values[1]
		s.dx = values[2]
		s.dy = values[3]
		s.dist = abs(s.dx - s.x) + abs(s.dy - s.y)

		sensors.append(s)
		aabb.add_point(values[0], values[1])
		aabb.add_point(values[2], values[3])

	testY = 10 if isTest else 2000000

	intervals = []
	for s in sensors:
		d = abs(testY - s.y) 
		if d > s.dist:
			continue
		
		interval = [s.x - (s.dist - d), s.x + (s.dist - d)]
		intervals.append(interval)

	intervals = sorted(intervals, key=lambda x: x[0])

	toDelete = []
	for i in range(len(intervals)):
		if i in toDelete:
			continue
		for j in range(i+1, len(intervals)):
			if j in toDelete:
				continue
			
			a = intervals[i]
			b = intervals[j]
			if a[1] >= b[1]:
				toDelete.append(j)
			elif a[1] >= b[0]:
				a[1] = b[1]
				toDelete.append(j)

	merged = [intervals[x] for x in range(len(intervals)) if x not in toDelete]

	count = 0
	for m in merged:
		count += m[1] - m[0]

	print(count)


def main_2(inp):
	sensors = []
	aabb = AABB()
	for line in inp:
		values = [int(x) for x in re.match("Sensor at x=(\-?[0-9]*), y=(\-?[0-9]*): closest beacon is at x=(\-?[0-9]*), y=(\-?[0-9]*)", line).groups()]
		s = Sensor()
		s.x = values[0]
		s.y = values[1]
		s.dx = values[2]
		s.dy = values[3]
		s.dist = abs(s.dx - s.x) + abs(s.dy - s.y)

		sensors.append(s)
		aabb.add_point(values[0], values[1])
		aabb.add_point(values[2], values[3])

	bound = 20 if isTest else 4000000

	count = 0
	for i in range(len(sensors)):
		# candidate points are 1 outside the snesing range for every sensor
		outDist = sensors[i].dist+1
		for y in range(sensors[i].y-outDist, sensors[i].y+outDist+1):
			points = []
			dx = outDist - (abs(sensors[i].y - y))
			points.append([sensors[i].x-dx, y])
			points.append([sensors[i].x+dx, y])
			if count % 100000 == 0:
				print(count, "points and counting...")
			for pt in points:
				count += 1
				if pt[0] < 0 or pt[0] > bound or pt[1] < 0 or pt[1] > bound:
					continue
				found = True
				for j in range(0, len(sensors)):
					if i == j:
						continue
					dist = abs(sensors[j].x - pt[0]) + abs(sensors[j].y - pt[1])
					if dist <= sensors[j].dist:
						found = False
						break
				if found:
					print(pt, 4000000*pt[0]+pt[1])
					return

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
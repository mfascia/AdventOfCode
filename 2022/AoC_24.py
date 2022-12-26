import os
import sys
import math
from queue import Queue


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
#-----------------------------------------------------------------------------------------------


NEIGHBOURS =[[0, 0], [0, -1], [1, 0], [-1, 0], [0, 1]]

class Valley:
	def __init__(self):
		self.blizzards = {
			">":[],
			"<":[],
			"v":[],
			"^":[]
		}
		self.sx = 0
		self.sy = 0
		self.period = 0
		self.history = {}

	def read_input(self, inp):
		self.sx = len(inp[0])-2
		self.sy = len(inp)-2
		y=0
		# ignoring the # all around the valley durnig parsing
		for line in inp[1:-1]:
			for x in range(1, len(line)-1):
				if line[x] in "><v^":
					self.blizzards[line[x]].append((x-1, y))
			y += 1

		self.period = math.lcm(self.sx, self.sy)
		self.history = {}
		for t in range(self.period):
			s = self.calc_state(t)
			self.history[t] = s

	def calc_state(self, time):
		blizz = {}
		for b in self.blizzards[">"]:
			x = (b[0]+time) % self.sx
			blizz[(x, b[1])] = ">"
		for b in self.blizzards["<"]:
			x = (b[0]-time) % self.sx
			blizz[(x, b[1])] = "<"
		for b in self.blizzards["v"]:
			y = (b[1]+time) % self.sy
			blizz[(b[0], y)] = "v"
		for b in self.blizzards["^"]:
			y = (b[1]-time) % self.sy
			blizz[(b[0], y)] = "^"
		return blizz

	def print_state(self, state):
		for y in range(self.sy):
			line = ""
			for x in range(self.sx):
				if (x, y) in state:
					line += state[(x, y)]
				else:
					line += "."
			print(line)
		print()

	def calc_fastest_travel_time(self, ps, pe, ts):
		next = []
		next.append((ps, ts))
		while len(next) > 0:
			c = next.pop(0)
			p = c[0]
			t = c[1]
			if p == pe:
				break
			neighbours = [tuple(n) for n in map(lambda k: (p[0]+k[0], p[1]+k[1]), NEIGHBOURS) if (n==ps) or (n==pe) or (n[0]>=0 and n[0]<self.sx and n[1]>=0 and n[1]<self.sy)]
			s = self.history[(t+1) % self.period]
			for n in neighbours:
				if not n in s and not (n, t+1) in next:		
					next.append((n, t+1))
		return t


def main(inp):
	valley = Valley()
	valley.read_input(inp)

	ps = (0, -1)
	pe = (valley.sx-1, valley.sy)

	t0 = valley.calc_fastest_travel_time(ps, pe, 0)
	t1 = valley.calc_fastest_travel_time(pe, ps, t0)
	t2 = valley.calc_fastest_travel_time(ps, pe, t1)
	print(t0, t1, t2)


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
			print ("--- Test #" + str(t+1) + "------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)
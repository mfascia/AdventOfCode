import os
import sys
import re
import copy


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


class Blueprint:
	def __init__(self):
		self.id = 0
		self.ore_ore = 0
		self.clay_ore = 0
		self.obsidian_ore = 0
		self.obsidian_clay = 0
		self.geode_ore = 0
		self.geode_obsidian = 0

class State:
	def __init__(self):
		self.parent = None
		self.time = 0
		self.ore = 0
		self.clay = 0
		self.obsidian = 0
		self.geode = 0
		self.robots_ore = 1
		self.robots_clay = 0
		self.robots_obsidian = 0
		self.robots_geode = 0


	def __str__(self):
		return	"time: "  + str(self.time) + ", " + \
				"resources: [" + str(self.ore) + ", " + str(self.clay) + ", " + str(self.obsidian) + ", " + str(self.geode) + "], " + \
				"robots: [" + str(self.robots_ore)  + ", " + str(self.robots_clay) + ", " + str(self.robots_obsidian)  + ", " + str(self.robots_geode) + "]" 


	def __repr__(self):
		return str(self)


	def tick(self):
		self.time += 1
		self.ore += self.robots_ore
		self.clay += self.robots_clay
		self.obsidian += self.robots_obsidian
		self.geode += self.robots_geode


	def next(self, blueprint, timeLimit, currMax=0):
		states = []

		# assuming we can build a geode robot every remaining minute, can we beat the current max?
		# if not, bail
		timeLeft = timeLimit - self.time
		if currMax >= self.geode + int(timeLeft*(timeLeft+1)*0.5) + self.robots_geode*timeLeft:
			return []

		# try make and geode robot if we can produce ore and obsidian
		if self.robots_obsidian > 0 and self.robots_ore > 0:
			s = copy.copy(self)
			s.parent = self
			while s.obsidian < blueprint.geode_obsidian or s.ore < blueprint.geode_ore:
				s.tick()
			if s.time < timeLimit-1:	# it will take at best 1 minutes for this new robot to contribute towards a geode (robot_geode > geode)
				s.tick()
				s.obsidian -= blueprint.geode_obsidian
				s.ore -= blueprint.geode_ore
				s.robots_geode += 1
				states.append(s)
				
		# try make an obsidian robot if we can produce ore and clay and we are bottlenecked by obsidian production
		if self.robots_clay > 0 and self.robots_ore > 0 and self.robots_obsidian < blueprint.geode_obsidian:
			s = copy.copy(self)
			s.parent = self
			while s.clay < blueprint.obsidian_clay or s.ore < blueprint.obsidian_ore:
				s.tick()
			if s.time < timeLimit-3:	# it will take at best 3 minutes for this new robot to contribute towards a geode (robot_obsidian > obsidian > robot_geode > geode)
				s.tick()
				s.clay -= blueprint.obsidian_clay
				s.ore -= blueprint.obsidian_ore
				s.robots_obsidian += 1
				states.append(s)

		# try building clay robot and we are bottlenecked by clay production
		if self.robots_ore > 0 and self.robots_clay < blueprint.obsidian_clay:
			s = copy.copy(self)
			s.parent = self
			while s.ore < blueprint.clay_ore:
				s.tick()
			if s.time < timeLimit-5:	# it will take at best 5 minutes for this new robot to contribute towards a geode (robot_clay > clay > robot_obsidian > obsidian > robot_geode > geode)
				s.tick()
				s.ore -= blueprint.clay_ore
				s.robots_clay += 1
				states.append(s)

		# try building ore robot and we are bottlenecked by ore production
		#if self.robots_ore > 0 and self.robots_ore < blueprint.clay_ore:
		if self.robots_ore > 0 and self.robots_clay == 0:		# this is faster but I'm not sure it works with different input data
			s = copy.copy(self)
			s.parent = self
			while s.ore < blueprint.ore_ore:
				s.tick()
			if s.time < timeLimit-1:
				s.tick()
				s.ore -= blueprint.ore_ore
				s.robots_ore += 1
				states.append(s)
		
		return states


def read_blueprints(inp):
	blueprints = {}
	for line in inp:
		bp = Blueprint()
		m = re.match("Blueprint ([0-9]*): Each ore robot costs ([0-9]*) ore. Each clay robot costs ([0-9]*) ore. Each obsidian robot costs ([0-9]*) ore and ([0-9]*) clay. Each geode robot costs ([0-9]*) ore and ([0-9]*) obsidian.", line)
		bp.id = int(m.groups()[0])
		bp.ore_ore = int(m.groups()[1])
		bp.clay_ore = int(m.groups()[2])
		bp.obsidian_ore = int(m.groups()[3])
		bp.obsidian_clay = int(m.groups()[4])
		bp.geode_ore = int(m.groups()[5])
		bp.geode_obsidian = int(m.groups()[6])
		blueprints[bp.id] = bp
	return blueprints


def main_1(inp):
	blueprints = read_blueprints(inp)

	q = 0

	for bp in blueprints.values():
		maxGeode = 0
		maxState = None

		s = State()
		next = []
		next.append(s)
		while len(next) > 0:
			st = next.pop(0)
			neighbours = st.next(bp, 24, maxGeode)
			if len(neighbours) == 0:
				while st.time < 24:
					st.tick()
				if maxGeode < st.geode:
					maxGeode = st.geode
					maxState = st
				continue
			for n in neighbours:
				if not n in next:		
					next.append(n)

		print("Evaluating Blueprint", bp.id, "Max geode(s):", maxGeode, "Details:", maxState)
		q += bp.id * maxGeode

	print("Sum of quality levels:", q)


def main_2(inp):
	blueprints = read_blueprints(inp)

	q = 1

	for bp in [x for x in blueprints.values()][0:3]:
		maxGeode = 0
		maxState = None

		s = State()
		next = []
		next.append(s)
		while len(next) > 0:
			st = next.pop()
			neighbours = st.next(bp, 32, maxGeode)	
			if len(neighbours) == 0:
				while st.time < 32:
					st.tick()
				if maxGeode < st.geode:
					maxGeode = st.geode
					maxState = st
				continue
			for n in neighbours:
				if not n in next:		
					next.append(n)

		print("Evaluating Blueprint", bp.id, "Max geode(s):", maxGeode, "Details:", maxState)
		q *= maxGeode

	print("result", q)


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
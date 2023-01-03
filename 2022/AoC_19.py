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

doTests = False
doInput = True
enablePart1 = True
enablePart2 = False
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


	def next(self, blueprint):
		if self.time >= 24:
			return []
		
		states = []
		# # collect from the robots that currently exist
		# self.tick()

		# always make geode robots if possible
		if self.robots_obsidian > 0 and self.robots_ore > 0:
			s = copy.copy(self)
			s.parent = self
			while s.obsidian < blueprint.geode_obsidian or s.ore < blueprint.geode_ore:
				s.tick()
			s.obsidian -= blueprint.geode_obsidian
			s.ore -= blueprint.geode_ore
			s.tick()
			s.robots_geode += 1
			states.append(s)

		# try building obsidian robot
		if self.robots_clay > 0 and self.robots_ore > 0:
			s = copy.copy(self)
			s.parent = self
			while s.clay < blueprint.obsidian_clay or s.ore < blueprint.obsidian_ore:
				s.tick()
			s.clay -= blueprint.obsidian_clay
			s.ore -= blueprint.obsidian_ore
			s.tick()
			s.robots_obsidian += 1
			states.append(s)

		# try building clay robot
		if self.robots_ore > 0:
			s = copy.copy(self)
			s.parent = self
			while s.ore < blueprint.clay_ore:
				s.tick()
			s.ore -= blueprint.clay_ore
			s.tick()
			s.robots_clay += 1
			states.append(s)

		# try building ore robot
		if self.robots_ore > 0  and self.robots_clay <= 1:
			s = copy.copy(self)
			while s.ore < blueprint.ore_ore:
				s.tick()
			s.ore -= blueprint.ore_ore
			s.tick()
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
	
	quality = []
	for bp in blueprints.values():
		maxGeode = 0
		maxState = None
		
		s = State()
		queue = [s]
		i = 0
		while i < len(queue):
			if queue[i].geode > maxGeode:
				maxGeode = queue[i].geode
				maxState = queue[i]
		
			nx = queue[i].next(bp)
			for n in nx:
				if n.time <= 24:		
					queue.append(n)
			i += 1
		
		print( maxGeode, bp.id, maxGeode * bp.id)
		
		s = maxState
		while s:
			print(s)
			s = s.parent
		print()
		
		quality.append(maxGeode * bp.id)

	print(sum(quality))


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
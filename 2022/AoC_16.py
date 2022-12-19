import os
import sys
import re
import queue


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


class Valve:

	def __init__(self):
		self.name = ""
		self.index = 0
		self.state = 0			# 0: closed, 1: open
		self.flowrate = 0
		self.tunnels = []

	def __str__(self):
		return "name: " + self.name + ", index=" + str(self.index) + ", flowrate=" + str(self.flowrate) + ", tunnels to " + ", ".join(self.tunnels)

	def __repr__(self):
		return str(self)


def parse_input(inp):
	valves = {}
	for line in inp:
		v = Valve()
		m = re.match("Valve ([A-Z][A-Z]) has flow rate=([0-9]*); tunnel(s*) lead(s*) to valve(s*) (.*)", line)
		v.name = m.groups()[0]
		v.index = len(valves)
		v.flowrate = int(m.groups()[1])
		v.tunnels = m.groups()[5].split(", ")
		valves[v.name] = v
		print(line)
		print(v)
		print()

	return valves


class State:

	def __init__(self):
		self.valves = None
		self.time = -1
		self.relief = -1
		self.location = None
		self.rpm = -1

	def copy(self, other):
		self.valves = [v for v in other.valves]
		self.time = other.time
		self.relief = other.relief
		self.location = other.location
		self.rpm = other.rpm

	def __lt__(self, other):
		if self.relief == other.relief:
			return self.rpm < other.rpm
		else:
			self.relief < other.relief

	def __eq__(self, other):
		return isinstance(other, type(self)) and self.valves == other.valves and self.relief == other.relief and self.location == other.location

	def __hash__(self):
			return hash((tuple(self.valves), self.relief, self.rpm, self.time))

	def __str__(self):
		return self.location + ", valves:" + str(self.valves) + ", time=" + str(self.time) + ", relief=" + str(self.relief)


def search(valves):
	costs = {}
	froms = {}

	start = State()
	start.valves = [0 for x in range(len(valves))]
	start.time = 1
	start.relief = 0
	start.location = "AA"
	start.rpm = 0

	costs[start] = 0
	froms[start] = None
	toVisit = queue.PriorityQueue()
	toVisit.put(start)

	worthyValves = sum([1 if x.flowrate > 0 else 0 for x in list(valves.values())])

	deadline = 30

	maxState = start

	while not toVisit.empty():
		cur = toVisit.get()
		# at any valve, if there is time left, it is possible to
		# - open the valve if it is closed
		# - move to one of the neighbouring valves
		# - stay where we are and let the pressure relief build up
		if cur.relief > maxState.relief:
			maxState = cur
			print(maxState)

		# if cur.time < deadline:
		# 	# open current valve if closed and worthy
		# 	if cur.valves[valves[cur.location].index] == 0 and valves[cur.location].flowrate > 0:
		# 		nxt = State()
		# 		nxt.copy(cur)
		# 		nxt.time += 1 
		# 		nxt.valves[valves[cur.location].index] = 1
		# 		nxt.rpm = cur.rpm + valves[nxt.location].flowrate 
		# 		nxt.relief = cur.relief + nxt.rpm
		# 		if nxt not in costs or costs[nxt] < nxt.relief:
		# 			costs[nxt] = nxt.relief
		# 			froms[nxt] = cur
		# 			toVisit.put(nxt)
		# 	# explore neighbours
		# 	if sum(cur.valves) < worthyValves:
		# 		for t in valves[cur.location].tunnels:
		# 			if cur.location == t:
		# 				continue
		# 			nxt = State()
		# 			nxt.copy(cur)
		# 			nxt.time += 1 
		# 			nxt.location = t 
		# 			nxt.relief = cur.relief + nxt.rpm
		# 			if nxt not in costs or costs[nxt] < nxt.relief:
		# 				costs[nxt] = nxt.relief
		# 				froms[nxt] = cur
		# 				toVisit.put(nxt)
		# 	else:
		# 		# sit there and let the pressure relief build up
		# 		nxt = State()
		# 		nxt.copy(cur)
		# 		nxt.time += 1 
		# 		nxt.relief = cur.relief + nxt.rpm
		# 		if nxt not in costs or costs[nxt] < nxt.relief:
		# 			costs[nxt] = nxt.relief
		# 			froms[nxt] = cur
		# 			toVisit.put(nxt)

		if cur.time < deadline:
			# explore neighbours
			if sum(cur.valves) < worthyValves and cur.time < deadline-1:
				for t in valves[cur.location].tunnels:
					nxt = State()
					nxt.copy(cur)
					nxt.time += 1 
					nxt.location = t
					nxt.relief = nxt.relief + nxt.rpm
					if valves[t].flowrate > 0 and nxt.valves[valves[t].index] == 0:
						nxt.time += 1 
						nxt.valves[valves[t].index] = 1
						nxt.rpm = nxt.rpm + valves[nxt.location].flowrate 
						nxt.relief = nxt.relief + nxt.rpm
					if nxt not in costs or costs[nxt] < nxt.relief:
						costs[nxt] = nxt.relief
						froms[nxt] = cur
						toVisit.put(nxt)
			elif cur.time < deadline:
				# sit there and let the pressure relief build up
				nxt = State()
				nxt.copy(cur)
				nxt.time += 1 
				nxt.relief = cur.relief + nxt.rpm
				if nxt not in costs or costs[nxt] < nxt.relief:
					costs[nxt] = nxt.relief
					froms[nxt] = cur
					toVisit.put(nxt)

	moves = []
	s = maxState
	while s != None:
		moves.append(s)
		s = froms[s]
	
	print()
	print("moves:")
	for m in reversed(moves):
		print(m)

	return froms


def main_1(inp):
	valves = parse_input(inp)
	search(valves)


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
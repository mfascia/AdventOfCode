import os
import sys
import itertools
from Queue import PriorityQueue


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


def create_unit(units, type, x, y):
				# type, pos
	units.append([type, (x, y)])


def parse_level(inp):
	units = []
	level = []
	for y in xrange(0, len(inp)):
		row = []
		for x in xrange(0, len(inp[y])):
			if inp[y][x] == "E":
				create_unit(units, "E", x, y)
			elif inp[y][x] == "G":
				create_unit(units, "G", x, y)
			row.append(inp[y][x])
		level.append(row)
	return level, units


def in_reading_order(a, b):
	if a[1] > b[1] or (a[1] == b[1] and a[0] > b[0]):
		return False
	else:
		return True


def navigate(level, unit, targets):
	frontier = [ [unit[1], 0] ]
	came_from = {}
	cost_so_far = {}
	hash = unit[1]
	came_from[hash] = None
	cost_so_far[hash] = 0

	dists = [1<<31 for x in targets]

	while frontier:
		frontier.sort(key=lambda x: (x[1], x[0][0], x[0][1]))
		current = frontier.pop()[0]

		if current in targets:
			dists[targets.index(current)] = min(dists[targets.index(current)], cost_so_far[current])

		neighbours = get_valid_neighbours(level, current) 
		for next in neighbours:
			new_cost = cost_so_far[current] + 1
			if next not in cost_so_far or new_cost < cost_so_far[next]:# or (new_cost == cost_so_far[next] and not in_reading_order(came_from[next], next)):
				cost_so_far[next] = new_cost
				frontier.append([next, new_cost])
				came_from[next] = current
	
	reachable = [targets[x] for x in xrange(0, len(targets)) if dists[x] != (1<<31)] 

	minDist = min(dists)
	if minDist == (1<<31):
		return reachable, unit[1], [unit[1]]

	target = targets[dists.index(minDist)]
	current = target
	path = [current]
	while current != unit[1]: 
		current = came_from[current]
		path.append(current)
	path.reverse() 

	return reachable, target, path[1:]


def get_unit_targets(level, units, unit):
	if unit[0] == "E":
		foes = [u for u in units if u[0] == "G"]
	else:
		foes = [u for u in units if u[0] == "E"]

	targets = set()
	for f in foes:
		n = get_valid_neighbours(level, f[1])
		for tgt in n:
			targets.add(tgt)
	targetList = list(targets)
	targetList.sort(key=lambda x: (x[1], x[0]))
	return targetList


def get_valid_neighbours(level, pos):
	possible = [(pos[0], pos[1]-1),	(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]+1)]
	return [x for x in possible if x[0] >= 0 and x[0] < len(level[0]) and x[1] >= 0 and x[1] < len(level) and level[x[1]][x[0]] == "."]


def print_level(level):
	for row in level:
		print "".join(row)


def print_unit(level, targets, reachable, nearest, next):
	for y in xrange(0, len(level)):
		row = level[y]
		s = ""
		for x in xrange(0, len(row)):
			if (x,y) == nearest:
				s += "!"
			elif (x,y) in reachable:
				s += "@"
			elif (x,y) in targets:
				s += "?"
			elif (x,y) == next:
				s += "n"
			else:
				s += row[x]
		print s


def main_1(inp):
	level, units = parse_level(inp)
	print_level(level)
	print

	for loop in xrange(0, 1):
		units.sort(key=lambda x: (x[1][1], x[1][0]))

		for u in units:
			targets = get_unit_targets(level, units, u)
			reachable, nearest, path = navigate(level, u, targets)
			print_unit(level, targets, reachable, nearest, path[0])
			if path:
				level[u[1][1]][u[1][0]] = "."
				level[path[0][1]][path[0][0]] = u[0]
				u[1] = path[0]
			print_level(level)
			print
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
					tests.append(read_input(testfile))
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			if enablePart1:
				print "--- Test #" + str(t+1) + ".1 ------------------------------"
				main_1(tests[t])
			if enablePart2:
				print "--- Test #" + str(t+1) + ".2 ------------------------------"
				main_2(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp)
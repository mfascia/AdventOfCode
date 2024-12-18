import os
import sys
import queue
import time
from collections import defaultdict

import AoC as aoc


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


MAX_COST = 100000000

ARROWS = {
	aoc.Vector(1, 0): ">",
	aoc.Vector(-1, 0): "<",
	aoc.Vector(0, 1): "v",
	aoc.Vector(0, -1): "^"
}


def print_maze(maze, bounds, start, end, path=[], drawArrows=True):
	txt = []
	for row in maze:
		txt.append("".join(row))

	for p in range(len(path)-1):
		if drawArrows:
			c = ARROWS[path[p+1]-path[p]] 
		else:
			c = "O"
		txt[path[p].y] = txt[path[p].y][:path[p].x] + c + txt[path[p].y][path[p].x+1:]

	txt[start.y] = txt[start.y][:start.x] + "S" + txt[start.y][start.x+1:]
	txt[end.y] = txt[end.y][:end.x] + "E" + txt[end.y][end.x+1:]

	for row in txt:
		print(row)
	print()


def parse(inp):
	width = len(inp[0])
	height = len(inp)
	maze = []
	for y in range(height):
		row = []
		for x in range(width):
			c = inp[y][x]
			row.append(c)
			if c == "S":
				start = aoc.Vector(x, y)
			elif c == "E":
				end = aoc.Vector(x, y)
		maze.append(row)
	return maze, [aoc.Vector(), aoc.Vector(width, height)], start, end


def neighbours(maze, bounds, pos, dir, cost):
	ret = []
	for ndir in aoc.ADJ_4:
		npos = pos + ndir
		if not npos.is_inside(*bounds) or maze[npos.y][npos.x] == "#":
			continue
		if ndir != dir:
			ret.append((npos, ndir, cost + 1000 + 1))
		else:
			ret.append((npos, ndir, cost + 1))
	return ret


def main_1(inp):
	maze, bounds, start, end = parse(inp)

	# Uses a simple Djikstra search. 
	# 	For each node being evaluated, it builds the path so far and pushes it on the queue
	# 	Cost is recorded per position without considering orientation
	#	Search ends when a path is found, as it is guaranteed to be (one of) the most optimal 
	# 						(they can be several of same cost, which is what part 2 is about)
	path = []
	open = queue.PriorityQueue()
	costs = defaultdict(lambda:MAX_COST)
	costs[start] = 0
	open.put((0, (start, aoc.Vector(1, 0)), []))

	score = 0
	while not open.empty():
		loc = open.get()
		cost, pos, dir, path = loc[0], *loc[1], loc[2]

		if pos == end:
			score = cost
			break

		costs[pos] = cost

		for npos, ndir, ncost in neighbours(maze, bounds, pos, dir, costs[pos]):
			if ncost < costs[npos]:
				tup = (ncost, (npos, ndir), path + [npos])
				open.put(tup)
	
	# print_maze(maze, bounds, start, end, path)
	print("score:", score)


def main_2(inp):
	maze, bounds, start, end = parse(inp)

	# Uses a modified Djikstra that will not stop after finding a path, but instead will continue 
	# with the same cost. 
	# For that, we keep track of the lowest cost of each positio and direction of travel
	t0 = time.time()
	open = queue.PriorityQueue()
	ss = (start, aoc.Vector(1, 0))
	costs = defaultdict(lambda: MAX_COST)
	costs[ss] = 0
	open.put((0, ss, [start]))
	
	best = MAX_COST
	paths = []

	while not open.empty():
		loc = open.get()
		cost, pos, dir, path = loc[0], *loc[1], loc[2]

		if cost > best:
			continue

		costs[(pos, dir)] = cost

		if pos == end:
			best = cost
			paths.append(path)

		for npos, ndir, ncost in neighbours(maze, bounds, pos, dir, costs[(pos, dir)]):
			if not npos in path and ncost < costs[(npos, ndir)]:
				tup = (ncost, (npos, ndir), path + [npos])
				open.put(tup)
	
	pts = set()
	for path in paths:
		for p in path:
			pts.add(p)
	# print_maze(maze, bounds, start, end, [x for x in pts], False)
	t1 = time.time()
	print("(took", t1-t0, "seconds)")
	print(len(pts))


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
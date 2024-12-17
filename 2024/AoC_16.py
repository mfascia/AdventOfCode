import os
import sys
import queue

import AoC as aoc




# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def vector_less_than(a, b):
	return a.x < b.x

aoc.Vector.__lt__ = vector_less_than


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


TDIR = {
	aoc.Vector(1, 0): ">",
	aoc.Vector(-1, 0): "<",
	aoc.Vector(0, 1): "v",
	aoc.Vector(0, -1): "^"
}

def print_maze(maze, bounds, path=[]):
	txt = []
	for row in maze:
		txt.append("".join(row))

	for p in range(len(path)):
		if p == 0:
			c = "S"
		elif p == len(path)-1:
			c = "E"
		else:
			c = TDIR[path[p+1]-path[p]]
		txt[path[p].y] = txt[path[p].y][:path[p].x] + c + txt[path[p].y][path[p].x+1:]

	for row in txt:
		print(row)


def unroll_path(pred, pos):
	path = []
	score = 0
	while pos:
		path.append(pos)
		pos = pred[pos]
	path.reverse()
	return path, score


def main_1(inp):
	maze, bounds, start, end = parse(inp)
	print_maze(maze, bounds)

	open = queue.PriorityQueue()
	cost = { start: 0 }
	pred = { start: None }
	open.put((0, (start, aoc.Vector(1, 0))))

	aoc.Vector.__lt__ = less

	path = []
	score = 0
	while not open.empty():
		loc = open.get()
		pos = loc[1][0]
		dir = loc[1][1]

		if pos == end:
			path, score = unroll_path(pred, pos)
			break

		for ndir in aoc.ADJ_4:
			npos = pos + ndir
			if not npos.is_inside(*bounds) or maze[npos.y][npos.x] == "#":
				continue
			if ndir != dir:
				ncost = cost[pos] + 1000 + 1
			else:
				ncost = cost[pos] + 1
	
			if not npos in cost or (ncost + h) < cost[npos]:
				pred[npos] = pos
				cost[npos] = ncost
				h = abs(end.x-npos.x) + abs(end.y-npos.y)
				tup = (ncost+h, (npos, ndir))
				if not tup in open.queue:
					open.put(tup)
	
	print_maze(maze, bounds, path)
	print("score:", score)


def search_rec(maze, bounds, end, pos, hitcount = {}, visited = [], path = []):
	visited.append(pos)
	if pos == end:
		for p in path:
			if p in hitcount:
				hitcount[p] += 1
			else:
				hitcount[p] = 1
		print("reached target")
	else:
		for ndir in aoc.ADJ_4:
			npos = pos + ndir
			if not npos.is_inside(*bounds) or maze[npos.y][npos.x] == "#" or npos in visited:
				continue
			search_rec(maze, bounds, end, npos, hitcount, visited, path + [npos])
	visited.pop()


def main_2(inp):
	maze, bounds, start, end = parse(inp)
	print_maze(maze, bounds)

	hitcount = {}
	search_rec(maze, bounds, end, start, hitcount)
	print(hitcount)
	

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
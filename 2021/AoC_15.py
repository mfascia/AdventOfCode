import os
import sys
import queue


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

# 4-adjacency neighbours
NEIGHBOURS =[[0, -1], [-1, 0], [1, 0],[0, 1]]


def find_shortest_path(grid):
	sx = len(grid[0])
	sy = len(grid)
	costs = {}
	froms = {}

	costs[(0,0)] = 0
	froms[(0,0)] = (-1,-1)
	toVisit = queue.PriorityQueue()
	toVisit.put([(0,0), 1])

	while not toVisit.empty():
		p = toVisit.get()[0]
		neighbours = [tuple(n) for n in map(lambda k: [p[0]+k[0], p[1]+k[1]], NEIGHBOURS) if n[0]>=0 and n[0]<sx and n[1]>=0 and n[1]<sy]
		for n in neighbours:
			c = costs[p] + grid[n[1]][n[0]]
			if n not in costs or costs[n] > c:
				costs[n] = c
				froms[n] = p
				toVisit.put([n, c])

	return costs[(sx-1, sy-1)]


def main_1(inp):
	grid = []
	for line in inp:
		grid.append([int(x) for x in line])
	print(find_shortest_path(grid))


def main_2(inp):
	grid = []
	for line in inp:
		grid.append([int(x) for x in line])

	sx = len(grid[0])
	sy = len(grid)

	exp = [[0 for x in range(0, 5*sx)] for y in range(0, 5*sy)]

	for y in range(0, sy):
		for x in range(0, sx):
			exp[y][x] = grid[y][x] 

	for y in range(0, sy):
		for x in range(sx, 5*sx):
			exp[y][x] = exp[y][x-sx] + 1
			if exp[y][x] == 10:
				exp[y][x] = 1

	for y in range(sy, 5*sy):
		for x in range(0, 5*sx):
			exp[y][x] = exp[y-sy][x] + 1
			if exp[y][x] == 10:
				exp[y][x] = 1

	print(find_shortest_path(exp))


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
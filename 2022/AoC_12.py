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
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


# 4-adjacency neighbours
NEIGHBOURS =[[0, -1], [-1, 0], [1, 0],[0, 1]]

def distance_from_point(grid, start, checkNeighbour=(lambda grid, a, b: True), cost=(lambda grid, a, b: 1)):
	sx = len(grid[0])
	sy = len(grid)
	costs = {}
	froms = {}

	costs[start] = 0
	froms[start] = (-1,-1)
	toVisit = queue.PriorityQueue()
	toVisit.put([start, 0])

	while not toVisit.empty():
		p = toVisit.get()[0]
		neighbours = [tuple(n) for n in map(lambda k: [p[0]+k[0], p[1]+k[1]], NEIGHBOURS) if n[0]>=0 and n[0]<sx and n[1]>=0 and n[1]<sy]
		for n in neighbours:
			if not checkNeighbour(grid, p, n):
				continue

			c = costs[p] + cost(grid, p, n)
			if n not in costs or costs[n] > c:
				costs[n] = c
				froms[n] = p
				toVisit.put([n, c])

	return froms


def find_shortest_path(grid, start, end, checkNeighbour=(lambda grid, a, b: True), cost=(lambda grid, a, b: 1)):
	froms = distance_from_point(grid, start, checkNeighbour, cost)

	path = []
	p = end
	while p != (-1, -1):
		path.append(p)
		p = froms[p]
	path = [x for x in reversed(path)]

	return path


def read_heightmap(inp):
	hm = []
	start = (-1, -1)
	end = (-1, -1)
	for y in range(len(inp)):
		txt = ""
		for x in range(len(inp[0])):
			c = inp[y][x]
			if c == "S":
				start = (x, y)
				c = "a"
			elif c == "E":
				end = (x, y)
				c = "z"
			txt += c
		hm.append(txt)
	return hm, start, end


def check_neighbour_going_up(grid, a, b):
	if (ord(grid[b[1]][b[0]]) > ord(grid[a[1]][a[0]]) + 1):
		return False
	return True


def main_1(inp):
	hm, start, end = read_heightmap(inp)

	for row in hm:
		print("".join(row))
	print(start, end)

	path = find_shortest_path(hm, start, end, checkNeighbour=check_neighbour_going_up )

	for y in range(len(inp)):
		txt = ""
		for x in range(len(inp[0])):
			if (x, y) in path:
				txt += "#"
			else:
				txt += "."
		print(txt)
	
	print(len(path)-1) # removing 1 to not count the starting position


def check_neighbour_going_down(grid, a, b):
	if (ord(grid[a[1]][a[0]]) > ord(grid[b[1]][b[0]]) + 1):
		return False
	return True


def main_2(inp):
	hm, start, end = read_heightmap(inp)

	for row in hm:
		print("".join(row))
	print(start, end)

	froms = distance_from_point(hm, end, check_neighbour_going_down )

	shortest = 1000000
	shortestPath = []

	for y in range(len(inp)):
		for x in range(len(inp[0])):
			if hm[y][x] == "a":
				path = []
				p = (x, y)
				print("Considering", p, "...")
				while p != (-1, -1):
					path.append(p)
					p = froms[p] if p in froms else (-1, -1)
				if len(path) > 1 and len(path) < shortest:
					shortest = len(path)
					shortestPath = path
				print("... and found a path of length", len(path))
	
	shortestPath = [x for x in reversed(shortestPath)]

	for y in range(len(inp)):
		txt = ""
		for x in range(len(inp[0])):
			if (x, y) in shortestPath:
				txt += "#"
			else:
				txt += "."
		print(txt)
	
	print(len(shortestPath)-1)


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
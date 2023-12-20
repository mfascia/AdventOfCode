import os
import sys
from queue import PriorityQueue


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


def parse_grid(text):
	grid = [[int(x) for x in y] for y in text]
	return grid, len(grid[0]), len(grid)


def print_grid(grid, width, height, path=None):
	for y in range(height):
		line = ""
		for x in range(width):
			if path and [x, y] in path:
				line += "@"
			else:
				line += str(grid[y][x])			
		print(line)


NEIGHBOURS = [
	[-1, 0],
	[+1, 0],
	[0, -1],
	[0, +1],
]


def manatthan(a, b):
	return max(a[0], b[0]) - min(a[0], b[0]) + max(a[1], b[1]) - min(a[1], b[1])


def astar(grid, width, height, start, end):
	open = PriorityQueue()
	open.put((0, start))

	key = tuple(start)
	cameFrom = { key: None }
	gscore = { key: 0 }
	fscore = { key: manatthan(start, end) }

	reached = False

	visited = 0
	while not open.empty():
		visited += 1

		# get next best node from queue
		_, pos = open.get()
		key = tuple(pos)
		print(pos)

		# check if reached our target
		if pos == end:
			reached = True
			break

		# fetch the last 3 moves
		hist = []
		prev = cameFrom[key]
		while prev and len(hist) < 3:
			hist.append(prev)
			prev = cameFrom[tuple(prev)]
		
		# check next possible moves
		for ndir in NEIGHBOURS:
			npos = [pos[0]+ndir[0], pos[1]+ndir[1]]
			nkey = tuple(npos)
		
			# no backtracking
			if key in cameFrom and npos == cameFrom[key]:
				continue

			# no going out of bounds
			if npos[0]<0 or npos[0]>=width or npos[1]<0 or npos[1]>=height:
				continue

			# no going straight for too long
			if len(hist) == 3:
				if npos[0] - hist[-1][0] == 4 or npos[0] - hist[-1][0] == -4 or npos[1] - hist[-1][1] == 4 or npos[1] - hist[-1][1] == -4:
					continue

			nscore = gscore[key] + grid[npos[1]][npos[0]]

			if (nkey not in gscore) or (nkey in gscore and nscore < gscore[nkey]):
				cameFrom[nkey] = pos
				gscore[nkey] = nscore
				fscore[nkey] = nscore + manatthan(npos, end)
				next = (fscore[nkey], npos)
				found = False
				open.put(next)
				print(pos, "-->", next)

	path = []
	lava = 0

	if reached:
		path.append(end)
		curr = cameFrom[tuple(end)]
		while curr != None:
			path.append(curr)
			curr = cameFrom[tuple(curr)]
		
		path = path[::-1]

		for p in path[1:]:
			lava += grid[p[1]][p[0]]

	print_grid(grid, width, height, path)

	print("path:", path)
	print("lava:", lava)
	print("visited:", visited)
	return path


# #state = [x, y, dx, dy, nbsteps, cost]
# def astar(grid, width, height, start, target):
# 	open = PriorityQueue()
# 	predecessor = {}

# 	initial = [start[0], start[1], 0, 0, 0, 0]
# 	predecessor[tuple(start)] = None
# 	open.put([0, initial])

# 	while open:
# 		# get next best node from queue
# 		_, state = open.get()
# 		#print(state)

# 		# unpack state for convenience
# 		pos = [state[0], state[1]]
# 		dir = [state[2], state[3]]
# 		steps = state[4]
# 		cost =  state[5]

# 		# check if reached our target
# 		if pos == target:
# 			break

# 		# check next possible moves
# 		for ndir in NEIGHBOURS:
# 			npos = [pos[0]+ndir[0], pos[1]+ndir[1]]
		
# 			# no backtracking
# 			if ndir == [-dir[0], -dir[1]]:
# 				continue

# 			# no going out of bounds
# 			if npos[0]<0 or npos[0]>=width or npos[1]<0 or npos[1]>=height:
# 				continue

# 			ncost = cost + grid[npos[1]][npos[0]]

# 			nkey = tuple(npos)
# 			if nkey in predecessor and predecessor[nkey] and ncost <= predecessor[nkey][5]:
# 				predecessor[nkey] = state

# 			open.put([ncost, [npos[0], npos[1], ndir[0], ndir[1], steps+1, ncost]])

# 			# if ndir == dir:
# 			# 	if steps == 2:
# 			# 		continue
# 			# 	else:
# 			# 		open.put([ncost, [npos[0], npos[1], ndir[0], ndir[1], steps+1, ncost]])
# 			# else:
# 			# 	open.put([ncost, [npos[0], npos[1], ndir[0], ndir[1], 0, ncost]])




def main_1(inp):
	grid, w, h = parse_grid(inp)
	astar(grid, w, h, [0, 0], [w-1, h-1])
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
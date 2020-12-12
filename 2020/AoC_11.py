import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def printGrid(grid):
	for row in grid:
		print("".join(row))
	print()

def main_1(inp):
	blank = ["." for x in range(0, len(inp[0])+2)]
	og = [[x for x in blank]]
	for line in inp:
		og.append(["."] + list(line) + ["."])  
	og += [[x for x in blank]]

	ng = [[v for v in row] for row in og]

	flip = 1
	while flip:
		flip = 0
		for y in range(1, len(og)-1):
			for x in range(1, len(og[0])-1):
				aE = 0
				aF = 0
				aO = 0
				for j in range(y-1, y+2):
					for i in range(x-1, x+2):
						if i == x and j == y:
							continue
						elif og[j][i] == ".":
							aF += 1
						elif og[j][i] == "L":
							aE += 1
						elif og[j][i] == "#":
							aO += 1
				if og[y][x] == "L":
					if aO == 0:
						ng[y][x] = "#"
						flip += 1
					else:
						ng[y][x] = "L"
				elif og[y][x] == "#":
					if aO >= 4:
						ng[y][x] = "L"
						flip += 1
					else:
						ng[y][x] = "#"
				elif og[y][x] == ".":
					ng[y][x] = "."

		tmp = og
		og = ng
		ng = tmp

	empty = 0
	occupied = 0
	floor = 0
	for y in range(0, len(og)):
		for x in range(0, len(og[0])):
			if og[y][x] == "L":
				empty += 1
			elif og[y][x] == "#":
				occupied += 1
			elif og[y][x] == ".":
				floor += 1
	print("# empty seats:", empty)
	print("# occupied seats:", occupied)
	print("# floor seats:", floor)


def buildAdjacency(grid, sx, sy, x, y):
	adj = [
		[".", ".", "."],
		[".", ".", "."], 
		[".", ".", "."] ]
	# right
	for i in range(x+1, sx):
		if grid[y][i] != ".":
			adj[1][2] = grid[y][i]
			break
	# left
	for i in range(x-1, 0, -1):
		if grid[y][i] != ".":
			adj[1][0] = grid[y][i] 
			break
	# down
	for i in range(y+1, sy):
		if grid[i][x] != ".":
			adj[2][1] = grid[i][x] 
			break
	# up
	for i in range(y-1, 0, -1):
		if grid[i][x] != ".":
			adj[0][1] = grid[i][x] 
			break
	i = 1
	# down and right
	while x+i < sx and y+i < sy:
		if grid[y+i][x+i] != ".":
			adj[2][2] = grid[y+i][x+i]
			break
		i += 1 
	i = 1
	# up and left
	while x-i > 0 and y-i > 0:
		if grid[y-i][x-i] != ".":
			adj[0][0] = grid[y-i][x-i] 
			break
		i += 1 
	i = 1
	# up and right
	while x+i < sx and y-i > 0:
		if grid[y-i][x+i] != ".":
			adj[0][2] = grid[y-i][x+i] 
			break
		i += 1 
	i = 1
	# down and left
	while x-i > 0 and y+i < sy:
		if grid[y+i][x-i] != ".":
			adj[2][0] = grid[y+i][x-i]
			break
		i += 1 
	return adj


def main_2(inp):
	blank = ["." for x in range(0, len(inp[0])+2)]
	og = [[x for x in blank]]
	for line in inp:
		og.append(["."] + list(line) + ["."])  
	og += [[x for x in blank]]

	ng = [[v for v in row] for row in og]

	sx = len(og[0])
	sy = len(og)

	flip = 1
	while flip:
		flip = 0
		for y in range(1, len(og)-1):
			for x in range(1, len(og[0])-1):
				aE = 0
				aF = 0
				aO = 0
				adj = buildAdjacency(og, sx, sy, x, y)
				for j in range(0, 3):
					for i in range(0, 3):
						if i == 1 and j == 1:
							continue
						elif adj[j][i] == ".":
							aF += 1
						elif adj[j][i] == "L":
							aE += 1
						elif adj[j][i] == "#":
							aO += 1
				if og[y][x] == "L":
					if aO == 0:
						ng[y][x] = "#"
						flip += 1
					else:
						ng[y][x] = "L"
				elif og[y][x] == "#":
					if aO >= 5:
						ng[y][x] = "L"
						flip += 1
					else:
						ng[y][x] = "#"
				elif og[y][x] == ".":
					ng[y][x] = "."

		tmp = og
		og = ng
		ng = tmp

	empty = 0
	occupied = 0
	floor = 0
	for y in range(0, len(og)):
		for x in range(0, len(og[0])):
			if og[y][x] == "L":
				empty += 1
			elif og[y][x] == "#":
				occupied += 1
			elif og[y][x] == ".":
				floor += 1
	print("# empty seats:", empty)
	print("# occupied seats:", occupied)
	print("# floor seats:", floor)



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
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)
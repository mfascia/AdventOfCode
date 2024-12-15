import os
import sys
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


def parse(inp):
	grid = []
	robot = aoc.Vector()
	moves = ""
	for y in range(len(inp)):
		if len(inp[y]) == 0:
			break
		else:
			row = []
			for x in range(len(inp[i])):
				if inp[y][x] == "@":
					robot = aoc.Vector(x, y)
					row.append(".")
				else:
					row.append(inp[y][x])

			grid.append(row)

	for yy in range(y+1, len(inp)):
		moves += inp[yy]

	return grid, robot, moves
	

def expand(grid):
	ngrid = []
	for y in range(len(grid)): 
		row = []
		for x in range(len(grid[0])): 
			if grid[y][x] == "#":
				row += "##"
			elif grid[y][x] == "O":
				row += "[]"
			elif grid[y][x] == ".":
				row += ".."
			elif grid[y][x] == "@":
				row += "@."
		ngrid.append(row)
	return ngrid


def print_grid(grid, robot):
	for y in range(len(grid)	):
		txt = ""
		for x in range(len(grid[0])):
			if robot == aoc.Vector(x, y):
				txt += "@"
			else:
				txt += grid[y][x]
		print(txt)
	print()


DIRS = {
	"^": aoc.Vector(0, -1),
	"v": aoc.Vector(0, 1),
	"<": aoc.Vector(-1, 0),
	">": aoc.Vector(1, 0)
}


def step1(grid, robot, dir):
	crates = 0
	np = robot+DIRS[dir]
	if grid[np.y][np.x] == ".":
		return np	
	elif grid[np.y][np.x] == "#":
		return robot
	else:
		p = np
		while grid[p.y][p.x] == "O":
			crates += 1
			grid[p.y][p.x] = "."
			p += DIRS[dir]
			if grid[p.y][p.x] == "#":
				p -= DIRS[dir]
		while crates > 0:
			grid[p.y][p.x] = "O"
			p -= DIRS[dir]
			crates -= 1
		return p


def gps(grid):
	gps = 0
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			if grid[y][x] in "O[":
				gps += 100*y + x
	return gps



def main_1(inp):
	grid, robot, moves = parse(inp)
	# print_grid(grid, robot)
	for m in moves:
		robot = step1(grid, robot, m)
	# print_grid(grid, robot)
	print("gps:", gps(grid))


def can_push(grid, pos, dir):
	if grid[pos.y][pos.x] == ".":
		return True
	elif grid[pos.y][pos.x] == "#":
		return False
	else:
		if grid[pos.y][pos.x] == "[":
			pos2 = pos + aoc.Vector(1, 0)
		else:
			pos2 = pos 	+ aoc.Vector(-1, 0)
		npos = pos + DIRS[dir]
		npos2 = pos2 + DIRS[dir]
		return can_push(grid, npos, dir) and can_push(grid, npos2, dir)


def do_push(grid, pos, dir):
	if not grid[pos.y][pos.x] in "[]":
		return
	if grid[pos.y][pos.x] == "[":
		pos2 = pos + aoc.Vector(1, 0)
	else:
		pos2 = pos 	+ aoc.Vector(-1, 0)
	npos = pos + DIRS[dir]
	npos2 = pos2 + DIRS[dir]
	do_push(grid, npos, dir)
	do_push(grid, npos2, dir)
	grid[npos.y][npos.x] = grid[pos.y][pos.x]
	grid[pos.y][pos.x] = "."
	grid[npos2.y][npos2.x] = grid[pos2.y][pos2.x]
	grid[pos2.y][pos2.x] = "."


def step2(grid, robot, dir):
	crates = 0
	np = robot+DIRS[dir]
	
	if grid[np.y][np.x] == ".":
		return np	
	elif grid[np.y][np.x] == "#":
		return robot
	elif dir in "<>":
		p = np
		while grid[p.y][p.x] in "[]":
			crates += 1
			grid[p.y][p.x] = "."
			p += DIRS[dir]
			grid[p.y][p.x] = "."
			p += DIRS[dir]
			if grid[p.y][p.x] == "#":
				p -= DIRS[dir]
		crate = int(crates/2)
		while crates > 0:
			grid[p.y][p.x] = "]" if dir == ">" else "["
			p -= DIRS[dir]
			grid[p.y][p.x] = "[" if dir == ">" else "]"
			p -= DIRS[dir]
			crates -= 1
		return p
	else:
		if can_push(grid, np, dir):
			do_push(grid, np, dir)
			return robot + DIRS[dir]
		else:
			return robot


def main_2(inp):
	grid, robot, moves = parse(inp)
	grid = expand(grid)
	robot.x *= 2
	# print_grid(grid, robot)
	for m in moves:
		robot = step2(grid, robot, m)
	# print_grid(grid, robot)
	print("gps:", gps(grid))


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
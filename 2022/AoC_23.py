import os
import sys


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


def has_neighbours(elves, p):
	for np in map(lambda n: (p[0]+n[0], p[1]+n[1]), [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]):
		if np in elves:
			return True
	return False	


def try_move_north(elves, pos):
	for off in [(-1, -1), (0, -1), (1, -1)]:
		np = (pos[0] + off[0], pos[1] + off[1])
		if np in elves:
			return False, pos
	return True, (pos[0], pos[1]-1)


def try_move_south(elves, pos):
	for off in [(-1, 1), (0, 1), (1, 1)]:
		np = (pos[0] + off[0], pos[1] + off[1])
		if np in elves:
			return False, pos
	return True, (pos[0], pos[1]+1)


def try_move_west(elves, pos):
	for off in [(-1, -1), (-1, 0), (-1, 1)]:
		np = (pos[0] + off[0], pos[1] + off[1])
		if np in elves:
			return False, pos
	return True, (pos[0]-1, pos[1])


def try_move_east(elves, pos):
	for off in [(1, -1), (1, 0), (1, 1)]:
		np = (pos[0] + off[0], pos[1] + off[1])
		if np in elves:
			return False, pos
	return True, (pos[0]+1, pos[1])


RULES = [
	try_move_north,
	try_move_south,
	try_move_west,
	try_move_east
]


def step(elves, round):
	proposed = {}
	stills = 0
	for e in elves.keys():
		if not has_neighbours(elves, e):
			proposed[e] = [e]
			stills += 1
			continue

		moved = False
		for r in range(round, round+4):
			ri = r % len(RULES)
			res, pos = RULES[ri](elves, e)
			if res:
				moved = True
				if pos in proposed:
					proposed[pos].append(e)
				else:
					proposed[pos] = [e]
				break
		if not moved:
			proposed[e] = [e]

	moved = {}
	for p, es in proposed.items():
		if len(es) == 1:
			moved[p] = 1
		else:
			for e in es:
				moved[e] = 1

	return moved, (stills == len(elves))


def calc_bounds(elves, width=0, height=0):
	bounds = [100000, 100000, width, height]
	for e in elves.keys():
		bounds[0] = min(bounds[0], e[0])
		bounds[1] = min(bounds[1], e[1])
		bounds[2] = max(bounds[2], e[0])
		bounds[3] = max(bounds[3], e[1])
	return bounds


def print_elves(elves, bounds=None):
	if not bounds:
		bounds = calc_bounds(elves)
	
	for y in range(bounds[1], bounds[3]+1):
		line = ""
		for x in range(bounds[0], bounds[2]+1):
			if (x, y) in elves:
				line += "#"
			else:
				line += "."
		print(line)
	print()


def read_elves(inp):
	elves = {}
	y = 0
	for line in inp:
		for x in range(len(line)):
			if line[x] == "#":
				elves[(x, y)] = 1
		y += 1

	w = len(inp[0])
	h = len(inp)

	return elves, w, h


def main_1(inp):
	elves, w, h = read_elves(inp)

	if isTest:
		print_elves(elves)

	for round in range(0, 10):
		elves, _ = step(elves, round)
		bounds = calc_bounds(elves, w, h)
		if isTest:
			print("End of round", round, ". Started at rule", round % len(RULES))
			print_elves(elves, bounds)

	bounds = calc_bounds(elves)
	empty = 0
	for y in range(bounds[1], bounds[3]+1):
		for x in range(bounds[0], bounds[2]+1):
			if (x, y) not in elves:
				empty += 1
	
	print(empty)


def main_2(inp):
	elves, w, h = read_elves(inp)

	if isTest:
		print_elves(elves)

	round = 0
	while True:
		elves, ended = step(elves, round)
		if ended:
			break
		round += 1

	print(round+1)


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
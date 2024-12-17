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
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


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


def print_maze(maze, bounds, path):
	txt = []
	for row in maze:
		txt.append("".join(row))

	for p in path:
		txt[p[0].y] = txt[p[0].y][:p[0].x] + p[1] + txt[p[0].y][p[0].x+1:]

	for row in txt:
		print(row)


def main_1(inp):
	maze, bounds, start, end = parse(inp)
	path = [[start, "S"], [end, "E"]]
	print_maze(maze, bounds, path)


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
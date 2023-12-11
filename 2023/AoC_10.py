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
#-----------------------------------------------------------------------------------------------


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# Reminder: Positive Y goes down 

VALID = {
	"S": [(1, 0), (-1, 0), (0, 1), (0, -1)],
	"|": [(0, 1), (0, -1)],
	"-": [(1, 0), (-1, 0)],
	"L": [(1, 0), (0, -1)],
	"J": [(-1, 0), (0, -1)],
	"7": [(-1, 0), (0, 1)],
	"F": [(1, 0), (0, 1)],
	".": []
 }


NEIGHBOURS = [
	[-1, 0],
	[+1, 0],
	[0, -1],
	[0, +1],
]


def parse_pipes(text):
	w = len(text[0]) + 2
	h = len(text) + 2
	pipes = ["." + y + "."for y in text]
	pipes.insert(0, "".join(["." for x in range(w)]))
	pipes.append("".join(["." for x in range(w)]))
	
	sx = -1
	sy = -1
	for y in range(h):
		for x in range(w):
			if pipes[y][x] == "S":
				sx = x
				sy = y
				break
	return w, h, pipes, sx, sy


def print_pipes(pipes):
	for y in range(len(pipes)):
		print("".join(pipes[y]))


def print_distancefield(pipes, flood, df, furthest):
	for y in range(len(df)):
		line = ""
		for x in range(len(df[0])):
			d = df[y][x]
			if d == -1:
				if flood[y][x] == 0:
					line += "I"
				elif flood[y][x] == 2:
					line += "O"
			elif d == furthest:
				line += "@"
			elif pipes[y][x] in ".S-|JL7F":
				line += ".S═║╝╚╗╔"[".S-|JL7F".find(pipes[y][x])]
		print(line)


def floodfill(grid, w, h, x, y, valid, c):
	queue = [(x, y)]
	while len(queue) > 0:
		px, py = queue.pop()
		if grid[py][px] == valid and grid[py][px] != c:
			grid[py][px] = c
			neighbours = [tuple(n) for n in map(lambda k: (px+k[0], py+k[1]), NEIGHBOURS) if n[0]>=0 and n[0]<w and n[1]>=0 and n[1]<h]
			for n in neighbours:
				if grid[n[1]][n[0]] != c:
					queue.append(n)


def explore(pipes, w, h, sx, sy):
	df = [[-1 for x in pipes[0]] for y in pipes]
	df[sy][sx] = 0
	prev = (-1, -1)
	curr = (sx, sy)
	next = (-1, -1)
	looped = False
	loop = []	
	while not looped > 0:
		for n in VALID[pipes[curr[1]][curr[0]]]:
			next = (curr[0] + n[0], curr[1] + n[1])
			if next[0] < 0 or next[0] >= w or next[1] < 0 or next[1] >= h:
				# no going out of bounds
				continue
			if (curr[0]-next[0], curr[1]-next[1]) not in VALID[pipes[next[1]][next[0]]]:
				# next needs to be actually connected to curr (solves the S case)
				continue
			elif pipes[next[1]][next[0]] == ".":
				# no exploring outside of pipes network
				continue
			elif next == prev:
				# no going backwards
				continue
			elif next[1] == sy and next[0] == sx:
				# reached the start, loop is complete
				loop.append(curr)
				looped = True
				break
			else:
				df[next[1]][next[0]] = df[curr[1]][curr[0]] + 1
				loop.append(curr)
				prev = curr
				curr = next
				break

	furthest = (max(max(y) for y in df) + 1) // 2
	print("Part 1: furthest =", furthest)
	
	if isTest:
		print()

	zoomed = [[0 for x in range(3*w)] for y in range(3*h)]
	for p in loop:
		x = p[0]
		y = p[1]
		zx = x*3+1
		zy = y*3+1
		pipe = pipes[y][x] 
		zoomed[zy][zx] = 1
		if pipe == "S":
			zoomed[zy-1][zx-1] = 1
			zoomed[zy][zx-1] = 1
			zoomed[zy+1][zx-1] = 1
			zoomed[zy-1][zx] = 1
			zoomed[zy+1][zx] = 1
			zoomed[zy-1][zx+1] = 1
			zoomed[zy][zx+1] = 1
			zoomed[zy+1][zx+1] = 1
		elif pipe == "|":
			zoomed[zy-1][zx] = 1
			zoomed[zy+1][zx] = 1
		elif pipe == "-":
			zoomed[zy][zx-1] = 1
			zoomed[zy][zx+1] = 1
		elif pipe == "J":
			zoomed[zy][zx-1] = 1
			zoomed[zy-1][zx] = 1
		elif pipe == "L":
			zoomed[zy][zx+1] = 1
			zoomed[zy-1][zx] = 1
		elif pipe == "7":
			zoomed[zy][zx-1] = 1
			zoomed[zy+1][zx] = 1
		elif pipe == "F":
			zoomed[zy][zx+1] = 1
			zoomed[zy+1][zx] = 1

	# (0, 0) is guaranteed to be outside as we pad the grid when parsing
	floodfill(zoomed, w*3, h*3, 0, 0, 0, 2)

	dezoomed = [[0 for x in range(w)] for y in range(h)]

	count = 0
	for y in range(h):
		for x in range(w):
			dezoomed[y][x] = zoomed[3*y+1][3*x+1]
			if dezoomed[y][x] == 0:
				count +=1 

	if isTest:
		print_distancefield(pipes, dezoomed, df, furthest)

	print("Part 2: caves = ", count)


def main(inp):
	width, height, pipes, sx, sy = parse_pipes(inp)
	if isTest:
		print_pipes(pipes)

	if sx != -1 and sy != -1:
		explore(pipes, width, height, sx, sy)


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
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		print ("--- Part 1 ------------------------------")
		main(inp)